# FIXIE - 1099 data extraction.

This script takes a 1099 Form in .pdf format as input, then extracts data from sections "Summary" (1099-DIV and 1099-B), and "Detail for Dividends and Distributions". Extracted data is converted to a Pandas dataframe, then grouped and summed by ticker symbol, then parsed to a pandas table. The output is a set of .csv files:
- `income.csv`. Displays data from 1099-DIV section details. Groups and sums tickers in rows with these columns:
    - nonqualified dividends
    - qualified dividends
    - short term capital gains
    - long term capital gains
    - section 199A dividends
    - foreign taxes paid
    - tax exempt income
- `summary.csv`. Extracts 1099-DIV section from the summary. 
- `broker_transactions.csv`. Extracts data from "Summary of Proceeds, Gains & Losses" section of the summary. Parses it in these columns:
    - Short term gain/loss
    - long term gain/loss
    - undetermined total
    - grand total

After completion, the script deletes copies made into `./input`, but leaves the original file untouched.
This tool complements a tax calculator spreadsheet. 

## Usage
0. [Python](https://www.python.org/downloads/) and [Java](https://www.java.com/en/download/help/download_options.html) are required dependencies installed on local machine.
1. `source venv/bin/activate` to activate virtual env.
2. `pip3 install -r requirements.txt` to install dependencies.
3. in main directory, create two empty folders: `./input` and `./output`.
4. drag a 1099 file (in .pdf format) into `./input` folder.
6. `python3 local.py` to run the program.
7. Find result files in `./output` folder.

## Use as a Quick Action for Mac

To be able to run this program as a Mac's Quick Action:
- Create an Automator Quick Action that points to `./driver.sh` (find an example script in `./automator.sh`).
- Add your quick action to your mac's Finder. 
- Right click on any file in Finder, the quick action you created should be displayed under 'Quick Actions' (tested on Mac OS X Sonoma 14.1.1).

## Contribute
Please clone, fork, contribute in any way you deem interesting.


