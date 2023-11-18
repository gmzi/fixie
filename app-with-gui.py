# THIS IS A DRAFT, the idea is to provide the user with a progress bar
# and error messages.

import os
import shutil
import sys
import pandas as pd
from cropFile import cropFile
from summary import extractSummary
from dividends_parser import dividends_parser
from broker_and_barter import broker_and_barter
import tkinter as tk
import tkinter.ttk as ttk


input_folder = './input/'



def process_files():
    global root

    # TO USE WITH A FILE MANUALLY ADDED TO INPUT FOLDER:
    files = os.listdir(input_folder)
    try:
        for file in files:
            if file.endswith('.pdf'):
                original_path = os.path.join(input_folder, file)
                new_path = os.path.join(input_folder, "data.pdf")
                shutil.copy(original_path, new_path)
    

        # TO USE WITH A RIGHT CLICKED FILE WITH AN AUTOMATOR QUICK ACTION:
        # if len(sys.argv) < 2:
        #     print('No file selected')
        #     sys.exit(1)

        # file_path = sys.argv[1]
        # try:
        #     if file_path.endswith('.pdf'):
        #         new_path = os.path.join(input_folder, "data.pdf")
        #         shutil.copy(file_path, new_path)
        #     else:
        #         print("The provided file is not a pdf")
        # except Exception as e:
        #     print(e)

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

        root.destroy()
    except Exception as e:
        print(e)
        root.destroy()

root = tk.Tk()
root.title("Processing")
root.geometry("300x100")

message_label = tk.Label(root, text="Fixie is working...")
message_label.pack(pady=20)

root.after(100, process_files)

root.mainloop()

# folder_path = "./output"
# subprocess.call(["open", folder_path])

