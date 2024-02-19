from datetime import datetime, timedelta
import pandas as pd
from pandas import json_normalize
import requests
import os


def get_historical_data(symbol, currency):
    
    def get_data(symbol, currency, last_date=None):
        try:

            # Make request to CryptoCompare API for each year of data
            current_year = datetime.now().year
            

            if last_date is not None:
                start_date = last_date + timedelta(days=1)
            else:
                start_date = datetime(2010, 1, 1)  # Start from the beginning if there's no last_date

            all_time_data = []
            
            for year in range(start_date.year, current_year + 1):
                end_date = datetime(year + 5, 1, 1)
                start_date = datetime(year, 1, 1)

                # Convert dates to Unix timestamp format
                end_date_unix = int(end_date.timestamp())
                start_date_unix = int(start_date.timestamp())

                # Make request to CryptoCompare API
                url = "https://min-api.cryptocompare.com/data/v2/histoday"
                parameters = {
                    "fsym": symbol,
                    "tsym": currency,
                    "limit": (end_date - start_date).days,
                    "toTs": end_date_unix,
                }
                response = requests.get(url, params=parameters)
                data = response.json()


                # Extract daily close prices
                for entry in data["Data"]["Data"]:
                    date = datetime.utcfromtimestamp(entry["time"]).strftime("%Y-%m-%d")
                    open_price = entry["open"]
                    high_price = entry["high"]
                    low_price = entry["low"]
                    close_price = entry["close"]
                    volume = entry["volumefrom"]
                    all_time_data.append([date, open_price, high_price, low_price, close_price, volume])
            return all_time_data
        except Exception as e:
            print("An error occurred:", e)
            return None
        
    filename = f"{symbol}_{currency}_data.parquet"
    if os.path.exists(filename):
        # Load the data from the parquet file
        df = pd.read_parquet(filename)
        
        # Get the current date and time
        time_now = datetime.now().strftime('%Y-%m-%d')

        last_date = df.index[-1].strftime('%Y-%m-%d')

        if  last_date == time_now:
            return df
        else:
            # Get the new data
            new_data = get_data(symbol, currency, last_date)
            # Convert the new data to a DataFrame
            new_df = pd.DataFrame(new_data, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
            
            # Concatenate the new data with the old data
            new_df['Date'] = pd.to_datetime(new_df['Date'])
            new_df = new_df.set_index("Date")  # Set Date column as index

           
            df = pd.concat([df, new_df]).sort_index()
            df = df[~df.index.duplicated(keep='last')]
            # Save the updated data to the parquet file
            df.to_parquet(filename)
            
            return df
    
    else:
        all_time_data = get_data(symbol, currency)
        
        df = pd.DataFrame(all_time_data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df["Date"] = pd.to_datetime(df["Date"])  # Convert Date column to datetime type
        df = df.set_index("Date")  # Set Date column as index
        df = df[~df.index.duplicated(keep='last')]
        df.to_parquet(filename)
        return df

def get_coinmetrics_data(symbol):
    
    def get_data(symbol, last_date=None):
        try:
            # Get today's date
            today = datetime.now().date()
            yesterday = today - timedelta(days=1)
                
            # Save yesterday's date as end_date
            end_date = yesterday.strftime('%Y-%m-%d')

            if last_date is not None:
                start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
            else:
                start_date = datetime(2010, 1, 1).strftime('%Y-%m-%d')  # Start from the beginning if there's no last_date

            metrics = "SplyCur,IssContNtv,CapMrktCurUSD,PriceUSD,DiffMean"
            
            # fetch the metrics
            data = requests.get(
                    f"https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets={symbol}&metrics={metrics}&start_time={start_date}&end_time={end_date}&frequency=1d&page_size=10000&pretty=true"
            ).json()

            data = json_normalize(data["data"])
            
            # Convert 'time' column to datetime type if it's not already
            data['time'] = pd.to_datetime(data['time'], utc=True)
            
            # Drop duplicate entries in 'time' column
            data = data.drop_duplicates(subset=['time'])
            
            # Set the 'time' column as the index
            data = data.set_index('time')
            
            # Format the index as strings with the desired format
            data.index = data.index.strftime('%Y-%m-%d')
            
            data.index = pd.to_datetime(data.index)
            data.rename(columns={"SplyCur": "tsupply", "IssContNtv": "issuance"}, inplace=True)
            data = data.astype({'tsupply': 'float', 'issuance': 'float', 'CapMrktCurUSD': 'float', 'DiffMean': 'float'})

            return data
        except Exception as e:
            print("An error occurred:", e)
            return None
        
    filename = f"{symbol}_S2F_data.parquet"
    if os.path.exists(filename):
        # Load the data from the parquet file
        df = pd.read_parquet(filename)
        
        # Get the current date and time
        time_now = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        last_date = df.index[-1].strftime('%Y-%m-%d')

        if  last_date == time_now:
            return df
        else:
            # Get the new data
            new_df = get_data(symbol, last_date)
            
            # Append the new data to the existing data
            df = pd.concat([df, new_df]).sort_index()
            df = df[~df.index.duplicated(keep='last')]
            # Save the updated data to the parquet file
            df.to_parquet(filename)
            
            return df
    
    else:
        df = get_data(symbol)
        
        df = df[~df.index.duplicated(keep='last')]
        
        df.to_parquet(filename)
        return df
        
#symbol = "BTC"
#currency = "USD"

#df = get_historical_data(symbol, currency)
#df = get_coinmetrics_data(symbol)

#display(df)    
