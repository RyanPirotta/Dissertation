import pandas as pd
from datetime import datetime

# To Display all Columns
pd.set_option('display.max_columns', None)

# Reading a CSV file and selecting the required fields
df_btc_prices_data = pd.read_csv(r'C:\Users\Ryan\Desktop\BTC_prices_dataset.csv',
                                 usecols=['Timestamp', 'Close', 'Volume_(BTC)', 'Volume_(Currency)', 'Weighted_Price'])

# Converting Timestamp in UTC
df_btc_prices_data['timestamp'] = [datetime.fromtimestamp(x) for x in df_btc_prices_data['Timestamp']]
df_btc_prices_data['timestamp'] = pd.to_datetime(df_btc_prices_data['timestamp'], utc=True)

# Drop UNIX Timestamp
df_btc_prices_data = df_btc_prices_data.drop(['Timestamp'], axis=1)

print(df_btc_prices_data)

# Exporting to Excel
df_btc_prices_data.to_csv(r'C:\Users\Ryan\Desktop\BTC_prices_cleaned.csv')
