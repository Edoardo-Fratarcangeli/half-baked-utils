from Utility.printMe import *
from Utility.printResult import *
from Calculators.total import *
from Input.collectors import *

if __name__ == "__main__":
    intro()
    state, income, expenses_list = CollectDataFromInput()
    result = analyze(state, income, expenses_list)
    printResult(result)

