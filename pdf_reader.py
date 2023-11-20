import PyPDF2
import tabula as tb
import pandas as pd

def cropFile(source, key_phrase, output):
    try: 
        with open(source, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            pdf_writer = PyPDF2.PdfWriter()
            num_pages = len(pdf_reader.pages)

            for page_num in range(num_pages):
                page_text = pdf_reader.pages[page_num].extract_text()
                if key_phrase in page_text:
                    page = pdf_reader.pages[page_num]
                    pdf_writer.add_page(page)

        if len(pdf_writer.pages) > 0:
            with open(output, 'wb') as output_file:
                pdf_writer.write(output_file)
            return True
        else: 
            print("cropping failed")
            return False
    except FileNotFoundError:
        print(f"Error: the file {source} was not found")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def summary(source):
    try:
        # Read pdf and extract table data:
        data = tb.read_pdf(source, pages='all', 
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

        return df
    except FileNotFoundError:
        print(f"Error: the file {source} was not found")
        return None
    except IndexError:
        print(f"Error: required data not found in the pdf")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def broker(source):
    try:
        data = tb.read_pdf(source, pages='all', 
                           area=[330, 20, 740, 850], 
                           columns=[100, 280, 400, 450, 550, 670, 671], 
                           pandas_options={'header': None}, 
                           stream=True, 
                           output_format='dataframe')

        narrow_data = data[0]

        narrow_data.columns = ['Term', 'Form_8949_type', 'Proceeds', 'Cost_basis', 'Market_discount', 'Wash_sale_loss_disallowed', 'drop_me', 'Net_gain_or_loss']

        filtered_rows = narrow_data[narrow_data['Form_8949_type'].str.contains('(?i)total|(?i)grand total', na=False)]

        final_data = filtered_rows[['Form_8949_type', 'Net_gain_or_loss']]

        short_term_total = final_data[final_data['Form_8949_type'].str.contains('Total Short-term')]['Net_gain_or_loss'].sum()
        long_term_total = final_data[final_data['Form_8949_type'].str.contains('Total Long-term')]['Net_gain_or_loss'].sum()
        undetermined_total = final_data[final_data['Form_8949_type'].str.contains('Total Undetermined-term')]['Net_gain_or_loss'].sum()
        grand_total = final_data[final_data['Form_8949_type'].str.contains('Grand total')]['Net_gain_or_loss'].sum()

        output_data = pd.DataFrame({
            'symbol': ['Broker Transactions'],
            'short term gain/loss': [short_term_total],
            'long term gain/loss': [long_term_total],
            'undetermined total': [undetermined_total],
            'grand total': [grand_total]
        })

        return output_data
    except FileNotFoundError:
        print(f"Error: the file {source} was not found")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def dividends(source):
    try: 
        data = tb.read_pdf(source, pages='all', area=(82, 20, 751, 600),
                           columns=[200, 250, 290, 400, 480], pandas_options={'header': None}, stream=True, output_format='dataframe')
        
        df = data[0]

        df.columns = ['description', 'cusip', 'symbol',
                      'date', 'amount', 'transaction']

        # clean rows:
        table_start = df[df['description'] ==
                         'Security description'].index.to_list()[0]
        df.drop(df.index[0:table_start], inplace=True)
        df = df.reset_index(drop=True)

        rows_to_drop_Secu = df[df['description'] ==
                               'Security description'].index
        df.drop(rows_to_drop_Secu, inplace=True)
        df = df.reset_index(drop=True)

        rows_to_drop_Cont = df[df['description'].str.contains(
            "(cont'd)", na=False)].index
        df.drop(rows_to_drop_Cont, inplace=True)
        df = df.reset_index(drop=True)

        rows_to_drop_Cont_ = df[df['date'].str.contains(
            "(contin)", na=False)].index
        df.drop(rows_to_drop_Cont_, inplace=True)
        df = df.reset_index(drop=True)

        # Create column to reference where Security starts tand ends
        df['Start/End'] = pd.Series(dtype='str')

        # Mark start and end of Securities by the "date" column. If there's a date, there's a valid value.
        empty_date_rows = df[df['date'].isna()]
        df.at[0, 'Start/End'] = 'start'

        # convert amounts to float values
        df['amount'] = df['amount'].apply(
            lambda x: float(x.replace(',', '')))

        # group Securities with a start and an end.
        for i, row in empty_date_rows.iterrows():
            if i == 0:
                df.at[i, 'Start/End'] = 'end'
            elif i == len(df) - 1:
                df.at[i, 'Start/End'] = 'start'
            else:
                df.at[i - 1, 'Start/End'] = 'end'
                df.at[i + 1, 'Start/End'] = 'start'

        # clean the redundant starts and ends
        df.loc[empty_date_rows.index, 'Start/End'] = ''

        # add marks to starts
        start_mask = df['Start/End'] == 'start'
        group_id = start_mask.cumsum()


        def sum_by_transaction_type(group_df):
            """Perform sums on each Security, sort by Transaction Type."""
            nonqualified_sum = group_df.loc[group_df['transaction']
                                            == 'Nonqualified dividend', 'amount'].sum()
            qualified_sum = group_df.loc[group_df['transaction']
                                         == 'Qualified dividend', 'amount'].sum()
            short_term = group_df.loc[group_df['transaction']
                                      == 'Short-term capital gain', 'amount'].sum()
            long_term = group_df.loc[group_df['transaction']
                                     == 'Long-term capital gain', 'amount'].sum()
            section_A = group_df.loc[group_df['transaction']
                                     == 'Section 199A dividend', 'amount'].sum()
            foreign_tax = group_df.loc[group_df['transaction']
                                       == 'Foreign tax withheld', 'amount'].sum()
            exempt_tax = group_df.loc[group_df['transaction']
                                      == 'Tax-exempt dividend', 'amount'].sum()
            symbol = group_df.iloc[0]['symbol']

            return pd.Series({
                'symbol': symbol,
                'nonqualified dividends': nonqualified_sum,
                'qualified dividends': qualified_sum,
                'short term capital gains': short_term,
                'long term capital gains': long_term,
                'section 199A dividends': section_A,
                'foreign taxes paid': foreign_tax,
                'tax exempt income': exempt_tax
            })

        # group results, clean index
        grouped_df = df.groupby(group_id).apply(
            sum_by_transaction_type).reset_index(drop=True)

        # Calculate the total value of each column of type 'float64'
        total_row = grouped_df.select_dtypes(include=['float64']).sum().to_frame().T
        total_row['symbol'] = '*** TOTALS ***'
        # Ensure the total_row columns order matches the grouped_df
        total_row = total_row[grouped_df.columns]
        # Add the totals row at the top of the DataFrame
        grouped_df = pd.concat([total_row, grouped_df], ignore_index=True)

        # format numbers on every row:
        for col in grouped_df.columns[1:]:
            grouped_df[col] = grouped_df[col].astype(float).map('${:,.2f}'.format)

        return grouped_df
    except FileNotFoundError:
        print(f"Error: the file {source} was not found")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None