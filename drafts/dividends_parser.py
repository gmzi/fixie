import tabula as tb
import pandas as pd

def dividends_parser(source):
    print("reading dividends...")

    # file = "./process/cropped.pdf"
    file = source
    data = tb.read_pdf(file, pages='all', area=(82, 20, 751, 600),
                       columns=[200, 250, 290, 400, 480], pandas_options={'header': None}, stream=True, output_format='dataframe')
    
    print("parsing dividends...")
    
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
        
        # return pd.Series({
        #     'symbol': symbol,
        #     'nonqualified dividends': '{:,.2f}'.format(nonqualified_sum),
        #     'qualified dividends': '{:,.2f}'.format(qualified_sum),
        #     'short term capital gains': '{:,.2f}'.format(short_term),
        #     'long term capital gains': '{:,.2f}'.format(long_term),
        #     'section 199A dividends': '{:,.2f}'.format(section_A),
        #     'foreign taxes paid': '{:,.2f}'.format(foreign_tax),
        #     'tax exempt income': '{:,.2f}'.format(exempt_tax)
        # })
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
    
    # add a row at the bottom with the total value of each column
    # total_row = grouped_df.select_dtypes(include=['float64']).sum()
    # total_row['symbol'] = '** totals **'
    # grouped_df = grouped_df._append(total_row, ignore_index=True)

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
    
    # export
    # grouped_df.to_csv(f"{output}/group.csv")
    # df.to_csv(f"{output}/data.csv")
    print('grouping done')
    return grouped_df


__all__ = ["dividends_parser"]