# FIXIE - 1099 Data Extraction

This script processes a 1099 form in .pdf format, extracting data from the 1099-DIV and 1099-B sections on the _Summary Information_ page. It also extracts data from the _Detail for Dividends and Distributions_ pages, grouping and summing by ticker symbol. The output is a set of .csv files:
- `summary.csv`. Extracts the 1099-DIV section from _Summary Information_ page. 
- `income.csv`. Displays data from the _Detail for Dividends and Distributions_ pages. Groups and sums rows by ticker symbol, with these columns:
    - Nonqualified dividends
    - Qualified dividends
    - Short term capital gains
    - Long term capital gains
    - Section 199A dividends
    - Foreign taxes paid
    - Tax exempt income
- `broker_transactions.csv`. Extracts data from the 1099-B section of the _Summary Information_ page ("Summary of Proceeds, Gains & Losses"), parsed into these columns:
    - Short term gain/loss
    - Long term gain/loss
    - Undetermined total
    - Grand total
- `result.xmls` is a single file combining the data described above into three worksheets.

## Processes
The script takes a PDF file, extracts specific sections into `./input`, then processes the data using PyPDF2 and tabula-py. After processing, it deletes the copies in `./input`, leaving the original file untouched, and stores output files into `./output`. This tool is a complement to a tax calculator spreadsheet. 

## Usage
0. [Python](https://www.python.org/downloads/) and [Java](https://www.java.com/en/download/help/download_options.html) are required dependencies for this program.
1. Activate the virtual environment: `source venv/bin/activate`.
2. Install dependencies: `pip3 install -r requirements.txt`. 
3. Create two empty folders in the main directory: `./input` and `./output`.
4. Place a 1099 file (in .pdf format) into the `./input` folder.
5. Go to `app.py` and change this line: `summary_table = summary('./input/summary.pdf', '2023')` for your desired year instead of "2023". Do the same in `local.py`. (Promise to fix this some day). 
5. Run the program: `python3 local.py`.
6. Find the result files in the `./output` folder.

## Use as a Quick Action for Mac

To use this program as a Quick Action on a Mac:
- Create an Automator Quick Action that points to `./driver.sh` (an example script and guide is provided in `./automator.sh`).
- Add your Quick Action to Finder on your Mac. 
- Right-click any file in Finder; the Quick Action you created should be displayed under 'Quick Actions' (tested on Mac OS X Sonoma 14.1.1).

## Contribute
Please feel free to clone, fork, or contribute in any way you find interesting.

## Related

Resources and related topics worth to investigate IMO:
- This [blogpost](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/?utm_source=tldrwebdev) with links to these cool tools: 
    - [ocr](https://tools.simonwillison.net/ocr)
    - [tesseract](https://github.com/tesseract-ocr/tesseract)
    - [PDF.js](https://mozilla.github.io/pdf.js/)