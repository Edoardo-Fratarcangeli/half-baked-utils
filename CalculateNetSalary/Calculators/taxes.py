import pandas as pd
import re

# ============================
# IRS 2025 - single filer
# ============================
federal_brackets = [
    (0, 11600, 0.10),
    (11600, 47150, 0.12),
    (47150, 100525, 0.22),
    (100525, 191950, 0.24),
    (191950, 243725, 0.32),
    (243725, 609350, 0.35),
    (609350, float("inf"), 0.37)
]

def calculateNetIncome(state, income):
    netIncome = income - ficaTax(income)
    netIncome = netIncome - federalTax(income)
    netIncome = netIncome - stateTax(income, state, filing_status="single")
    return netIncome

# FICA
def ficaTax(income):    
    social_security_cap = 168000
    ss_rate = 0.062
    medicare_rate = 0.0145
    medicare_additional_rate = 0.009  # sopra 200k
    
    ss_tax = min(income, social_security_cap) * ss_rate
    medicare_tax = income * medicare_rate
    if income > 200000:
        medicare_tax += (income - 200000) * medicare_additional_rate
    
    fica_total = ss_tax + medicare_tax
    return fica_total
    
def normalize_state_name(name):
    return re.sub(r'[^a-zA-Z]', '', str(name)).lower()

# State
def stateTax(income, state, filing_status):
    
    file_path = "ImportFiles/taxSheet.xlsx"
    states_data = read_state_tax_excel(file_path)

    state_row = None
    target = normalize_state_name(state)
    for st_name, data in states_data.items():
        if target in normalize_state_name(st_name):
            state_row = data
            break

    if state_row is None:
        print(f"Stato {state} non trovato, tassa statale 0.")
        return 0

    brackets = state_row["single_brackets"] if filing_status.lower()=="single" else state_row["married_brackets"]
    state_tax = 0
    previous_limit = 0
    for rate, limit in brackets:
        if income > previous_limit:
            taxable = min(income, limit) - previous_limit
            state_tax += taxable * rate
            previous_limit = limit
        else:
            break

    return state_tax * income

def read_state_tax_excel(file_path):

    # Downloaded from:
    # https://taxfoundation.org/data/all/state/state-income-tax-rates/

    df = pd.read_excel(file_path, header=None, skiprows=2)  # saltando le prime due righe di intestazioni

    states_data = {}
    current_state = None

    for i, row in df.iterrows():
        state_cell = row[0]
        # If cell is not empty update
        if pd.notna(state_cell):
            current_state = state_cell.strip()
            states_data[current_state] = {"single_brackets": [], "married_brackets": []}

            # Ignored deductions and personal exemption

        # End of state
        if current_state is None or pd.isna(row[1]):
            continue

        # ============================
        # Single
        # Colonna B = rate, colonna D = bracket
        # ============================
        rate_s = row[1]
        bracket_s = row[3]
        if pd.notna(rate_s) and pd.notna(bracket_s):
            rate_value = float(str(rate_s).replace("%",""))/100
            bracket_value = float(str(bracket_s).replace("$","").replace(",",""))
            states_data[current_state]["single_brackets"].append((rate_value, bracket_value))

        # ============================
        # Married
        # Colonna E = rate, colonna G = bracket
        # ============================
        rate_m = row[4]
        bracket_m = row[6]
        if pd.notna(rate_m) and pd.notna(bracket_m):
            rate_value = float(str(rate_m).replace("%",""))/100
            bracket_value = float(str(bracket_m).replace("$","").replace(",",""))
            states_data[current_state]["married_brackets"].append((rate_value, bracket_value))

    return states_data

# Federal
def federalTax(income):
    
    url = "https://www.irs.gov/filing/federal-income-tax-rates-and-brackets"
    
    tabelle = pd.read_html(url)
    
    # Assumption: first and only
    df = tabelle[0]
    
    df.columns = ['Tax Rate', 'From', 'Up To']
    
    # Clean
    brackets = []
    for _, row in df.iterrows():
        rate = float(str(row['Tax Rate']).replace('%','').strip()) / 100
        
        lower = float(str(row['From']).replace('$','').replace(',','').strip())
        
        up_text = str(row['Up To']).strip()
        if up_text.lower() in ['and up', 'and over', 'and higher']:
            upper = float('inf')
        else:
            upper = float(up_text.replace('$','').replace(',','').strip())
        
        brackets.append((lower, upper, rate))

    tax = 0
    for lower, upper, rate in brackets:
        if income > lower:
            # calcola quanto del reddito rientra nello scaglione
            taxable = min(income, upper) - lower
            tax += taxable * rate
        else:
            break  # se income <= lower, non tassare ulteriormente
    return tax
