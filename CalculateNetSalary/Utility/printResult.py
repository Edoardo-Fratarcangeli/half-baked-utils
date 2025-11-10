import pandas as pd
from enum import Enum
import matplotlib.pyplot as plt

class PrintFormat(Enum):
    Console = 1
    Pdf = 2
    Excel = 3

__all__ = ['printResult'] 

def printResult (results, format: PrintFormat = PrintFormat.Console):
    match format:
        case PrintFormat.Console :
            printResultConsole(results)
        case PrintFormat.Pdf:
            printResultPdf(results)
        case PrintFormat.Excel:
            printResultExcel(results)

def printResultConsole (results):
    df = pd.DataFrame(results)
    print(df)

def printResultPdf (results):

    filename="my_report.pdf"

    fig, ax = plt.subplots(figsize=(len(results.columns)*2, 2))  # adjust width for number of columns
    ax.axis('tight')
    ax.axis('off')
    
    # Create table
    table = ax.table(cellText=results.values, colLabels=results.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=list(range(len(results.columns))))
    
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    print(f"DataFrame exported to PDF: {filename}")
    
def printResultExcel (results):

    filename = "finance_report.xlsx"

    results.to_excel(filename, index=False)
    print(f"DataFrame exported to Excel: {filename}")
