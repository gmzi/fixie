import os
import shutil
import sys
import pandas as pd
from pdf_reader import cropFile, summary, broker, dividends, interest

def main():
    input_folder = './input/'

    # GRAB A FILE MANUALLY ADDED TO INPUT FOLDER:
    files = os.listdir(input_folder)
    file_name = 'default'

    try:
        for file in files:
            if file.endswith('.pdf'):
                original_path = os.path.join(input_folder, file)
                new_path = os.path.join(input_folder, "data.pdf")
                shutil.copy(original_path, new_path)
    except Exception as e:
        print(e)

    try: 
        summary_pdf = cropFile('./input/data.pdf', 
                       '1a- Total ordinary dividends (includes lines 1b, 5, 2e)',
                       './input/summary.pdf')
        income_pdf = cropFile("./input/data.pdf", 
                       'Detail for Dividends and Distributions', 
                       './input/income.pdf')
        interest_pdf = cropFile('./input/data.pdf',
                        'Interest Income',
                        './input/interest.pdf')
        
        if not summary_pdf:
            print("Crop failed at summary section")
            sys.exit(1)
        if not income_pdf:
            print("Crop failed at dividends section")
            sys.exit(1)
        
        summary_table = summary('./input/summary.pdf', '2023')
        broker_table = broker('./input/summary.pdf')
        income_table = dividends('./input/income.pdf')
        
        if interest_pdf:
            interest_table = interest('./input/interest.pdf')
            interest_table.to_csv(f'./output/interest_{file_name}.csv')

        # income_table.to_csv(f'./output/income_{file_name}.csv')
        # broker_table.to_csv(f'./output/broker_transactions_{file_name}.csv')
        
        # summary_table.to_csv(f'./output/summary_{file_name}.csv')

        # with pd.ExcelWriter(f'./output/result_{file_name}.xlsx', engine='xlsxwriter') as writer:
        #     income_table.to_excel(writer, sheet_name='Income', index=False)
        #     broker_table.to_excel(writer, sheet_name='Broker Transactions', index=False)
        #     summary_table.to_excel(writer, sheet_name='Summary', index=False)

    except Exception as e:
        print(e)
        sys.exit(1)
    
    folder_to_clean = "./input/"
    files_to_clean = ["data.pdf", "income.pdf", "summary.pdf", "interest.pdf"]
    for file_name in files_to_clean:
        file_path = os.path.join(folder_to_clean, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"File not found: {file_path}")
    
    print("Done")

if __name__ == '__main__':
    main()