from Calculators.taxes import calculateNetIncome
from  Calculators.expenses import expensesAndSum
import pandas as pd

# solo queste verranno importate con *
__all__ = ['analyze'] 

def analyze(state, income, expenses_list):
    netIncome = calculateNetIncome(state, income)
    expensesTotal_list = expensesAndSum(expenses_list)
    return CreateFinanceDataFrame(state, netIncome, expensesTotal_list)


def CreateFinanceDataFrame(state, net_income, expenses_list):

    # Ensure 'total' is last
    if expenses_list[-1][0].lower() != "total":
        total_expenses = sum(value for _, value in expenses_list)
        expenses_list.append(("total", total_expenses))
    else:
        total_expenses = expenses_list[-1][1]
        
    # Build columns: first 'State', then category names, then 'Net Remaining'
    columns = ["State"] + [name.capitalize() for name, _ in expenses_list] + ["Net Remaining"]
    
    # Build row values
    values = [state] + [value for _, value in expenses_list] + [net_income - total_expenses]
    
    # Create DataFrame
    df = pd.DataFrame([values], columns=columns)
    

    return df
