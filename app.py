import os
import shutil
import glob
import subprocess
import pandas as pd
from cropFile import cropFile
from summary import extractSummary
from dividends_parser import dividends_parser
from broker_and_barter import broker_and_barter

input_folder = './input/'
files = os.listdir(input_folder)

# duplicate user's file into `data.pdf`
try:
    for file in files:
        if file.endswith('.pdf'):
            original_path = os.path.join(input_folder, file)
            new_path = os.path.join(input_folder, "data.pdf")
            shutil.copy(original_path, new_path)
except Exception as e:
    print(e)
    
# Split 1099 file, store sections as separate pdf's:
summary_pdf = cropFile('./input/data.pdf', 
                       '1a- Total ordinary dividends (includes lines 1b, 5, 2e)',
                       './input/summary.pdf')

income_pdf = cropFile("./input/data.pdf", 
                       'Detail for Dividends and Distributions', 
                       './input/income.pdf')

# create Pandas tables from pdf sections
income_table = dividends_parser('./input/income.pdf')
broker_table = broker_and_barter('./input/summary.pdf')
summary_table = extractSummary('./input/summary.pdf')

# Export each table as a different .csv 
income_table.to_csv('./output/income.csv')
broker_table.to_csv('./output/broker_transactions.csv')
summary_table.to_csv('./output/summary.csv')


# Export each table as a worksheet in a single combined .xmls
with pd.ExcelWriter('./output/result.xlsx', engine='xlsxwriter') as writer:
    income_table.to_excel(writer, sheet_name='Income', index=False)
    broker_table.to_excel(writer, sheet_name='Broker Transactions', index=False)
    summary_table.to_excel(writer, sheet_name='Summary', index=False)


# clean input folder from section pdf's used for data extraction, leave the original untouched
folder_to_clean = "./input/"
files_to_clean = ["data.pdf", "income.pdf", "summary.pdf"]
for file_name in files_to_clean:
    file_path = os.path.join(folder_to_clean, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"File not found: {file_path}")


print('done')

# folder_path = "./output"
# subprocess.call(["open", folder_path])

