import tabula as tb
import pandas as pd

def extractSummary(source):

    file = source

    # Read pdf and extract table data:
    data = tb.read_pdf(file, pages='all', 
                       area=[82, 20, 751, 600], 
                       columns=[280, 301, 370],
                       pandas_options={'header': None}, 
                       stream=True, 
                       output_format='dataframe')
    
    narrow_data = data[0]
    
    narrow_data.columns = ['description', 'interm', 'amount', 'not-used']

    # Clean extracted data:
    df = pd.DataFrame(narrow_data)
    start_row = df[df['description'] == "DIVIDENDS AND DISTRIBUTIONS 2022 1099-DIV"].index.to_list()[0]
    end_row = df[df['description'] == "SUMMARY OF PROCEEDS, GAINS & LOSSES, ADJ"].index.to_list()[0]
    df = df.iloc[start_row+1:end_row]

    # Split long text into multiple lines in the "description" column
    max_line_width = 40 # Maximum width of each line in characters
    df["description"] = df["description"].apply(lambda x: "\n".join([x[i:i+max_line_width] for i in range(0, len(x), max_line_width)]) if isinstance(x, str) else x)

    # Preserve these two descriptions only:
    df = df[["description", "amount"]]

    # Export to .csv file:
    # df.to_csv(f"{output}/summary.csv", index=False)

    print("summary extraction done")
    
    return df

__all__ = ["extractSummary"]