import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
from coinmetrics.api_client import CoinMetricsClient
import warnings

warnings.filterwarnings("ignore")

def build_s2f(begin_timestamp, end_timestamp):
	# construct the Bitcoin Stock-to-Flow Ratio using the CoinMetrics API
	client = CoinMetricsClient()

	# string of format %Y-%m-%d also accepted
	if "datetime" in str(type(begin_timestamp)):
		begin_timestamp = begin_timestamp.strftime("%Y-%m-%d")
	if "datetime" in str(type(end_timestamp)):
		end_timestamp = end_timestamp.strftime("%Y-%m-%d")

	asset = "btc"
	# define the metrics to fetch
	metrics = "SplyCur,IssContNtv,CapMrktCurUSD,PriceUSD,DiffMean"
	# fetch the metrics
	asset_data = client.get_asset_metrics(assets=asset, metrics=metrics, start_time=begin_timestamp, end_time=end_timestamp)
	raw_data = pd.DataFrame(asset_data)
	# export raw data to csv
	#raw_data.to_csv("CM_raw_data.csv", encoding='utf-8')
	
	# do this dumbass bullshit because pandas resampling without datetimeindex blah blah
	mydates = pd.date_range(begin_timestamp, end_timestamp).tolist()
	mydates = pd.to_datetime(mydates, utc=True)
	mydates = pd.DatetimeIndex(mydates)

	# drop unecessary data
	raw_data.drop(['asset', 'time'], axis=1, inplace=True)
	# create new dataframe for export
	cleaned_data = pd.DataFrame(index=mydates, data=raw_data.values, columns=raw_data.columns)
	# rename columns to be more intuitive
	cleaned_data.rename(columns={"SplyCur": "tsupply", "IssContNtv": "issuance"}, inplace=True)
	# make sure all columns are of type float (recent API update was returning str)
	cleaned_data['tsupply'] = cleaned_data['tsupply'].astype(float)
	cleaned_data['issuance'] = cleaned_data['issuance'].astype(float)
	cleaned_data['CapMrktCurUSD'] = cleaned_data['CapMrktCurUSD'].astype(float)
	cleaned_data['DiffMean'] = cleaned_data['DiffMean'].astype(float)

	# add calculated values to the dataframe
	cleaned_data['lnMC'] = np.log(cleaned_data['CapMrktCurUSD'])
	cleaned_data['lndiff'] = np.log(cleaned_data['DiffMean'])
	cleaned_data['issuance_avg'] = cleaned_data['issuance'].resample('W').mean()
	cleaned_data['fwd_issuance'] = np.multiply(cleaned_data['issuance'], 365)
	cleaned_data['s2f'] = np.divide(cleaned_data[['tsupply']], cleaned_data[['fwd_issuance']])
	cleaned_data['lns2f'] = np.log(cleaned_data[['s2f']])
	# resample the data by week 
	cleaned_data = cleaned_data.resample('W').mean()

	return cleaned_data



