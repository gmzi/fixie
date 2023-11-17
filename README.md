# FIXIE data extractor

This script takes a 1099 Form in .pdf format as input, and extracts the section "Detail for Dividends and Distributions". From this section, the program extracts the data from the pdf (converts it to a Pandas dataframe), groups dividends and distributions by transaction type and sums them, the output is a .csv file that discriminates, for each ticker of the 1099, these columns: 

- nonqualified dividends
- qualified dividends
- short term capital gains
- long term capital gains
- section 199A dividends
- foreign taxes paid
- tax exempt income

Upon completion, the program creates a "group.csv" file with the sorted data; and a "data.csv" file and a "cropped.pdf" file, both for validation purposes.
The input file (the original 1099 form), is deleted from the input folder. 
Further processes are handled by __Fixie, porftolio tracking tool for fixed income lovers__ (find more on Learn folder).



## Usage
0. Python and Java are required dependencies on local computer. For Java installation, see [here](https://www.java.com/en/download/help/download_options.html); for Python installation [here](https://www.python.org/downloads/)
1. `source venv/bin/activate`.
2. install dependencies (`pip3 install -r requirements.txt`).
3. in main directory, create two folders: `/input` and `/output`.
4. drag a 1099 file into `./input` folder.
6. on root directory: `python3 app.py` to run program.
7. Find results in `/output` folder