import tabula as tb
import pandas as pd

def broker_and_barter(source):

    file = source

    data = tb.read_pdf(file, pages='all', 
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


    # output_data.to_csv('./output/broker.csv')


    return output_data

__all__ = ["broker_and_barter"]