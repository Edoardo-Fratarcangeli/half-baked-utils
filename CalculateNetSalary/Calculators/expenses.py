
# solo queste verranno importate con *
__all__ = ['analyze'] 

def expensesAndSum(expenses):

    # Calculate total of all expenses and append to the list
    total_expenses = sum(value for _, value in expenses)
    expenses.append(("total", total_expenses))

    return expenses
