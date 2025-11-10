# solo queste verranno importate con *
__all__ = ['CollectDataFromInput'] 

def CollectDataFromInput():
    try:
        income = float(input("Enter your annual gross income ($): "))
    except ValueError:
        print("Please enter a valid number.")
        exit()

    state = input("Enter the state (e.g., California): ").strip().lower()

    expenses_list = []
    print("Enter your monthly expenses. Type 'done' when finished.")
    while True:
        name = input("Expense name (Rent, Food, Car, Health Insurance, etc): ").strip().lower()
        if name.lower() == "done":
            break
        try:
            value = float(input(f"Monthly amount for {name} ($): "))
        except ValueError:
            print("Invalid value, please try again.")
            continue
        expenses_list.append((name, value))

    return state, income, expenses_list