import requests
import numpy as np
import pandas as pd
import time
import datetime
import os
from datetime import datetime
from pytz import timezone 
import pathlib
from utils import *
directory = str(pathlib.Path(__file__).parent.resolve())
from pathlib import Path

data_dir = Path("data/")
data_dir.mkdir(exist_ok=True)  # Creates directory if missing


class OptionChain():
    def __init__(self, symbol='NIFTY', timeout=5,expiry_date='30-Nov-2023',update_time=20,new_file=True) :
        self.new_file=new_file
        self.update_time=update_time
        self.base_path="../data/option_chain/"
        
        self.expiry_date=expiry_date
        self.symbol=symbol
        self.file_path=self.base_path+self.symbol+"_"+self.expiry_date+".csv"
        self.delta=50
        if(self.symbol==symbol):
            self.delta=100
        self.num_sum=5


        self.url = "https://www.nseindia.com/api/option-chain-indices?symbol={}".format(symbol)
        self.session = requests.sessions.Session()
        self.session.headers = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5" }
        self.timeout = timeout
        self.session.get("https://www.nseindia.com/option-chain", timeout=self.timeout)
        self.ce_oi=[]
        self.pe_oi=[]
        self.diff_oi=[]
        self.time_x=[]

        self.fetch_data()
        self.init_oi_array(K=15)        ###inital array





    def fetch_data(self, expiry_date=None, starting_strike_price=None, number_of_rows=2):
        try:
            data = self.session.get(url=self.url, timeout=self.timeout)
            data = data.json()
            df = pd.json_normalize(data['records']['data'])
            self.option_chain=df
            df=df[df.expiryDate==self.expiry_date]
            self.cur_option_chain=df
            #self.update_ois()

        except Exception as ex:
            print('Error: {}'.format(ex))
            try:
                self.session.get("https://www.nseindia.com/option-chain", timeout=self.timeout)
            
            except Exception as ex:
                print("error in getting session..")

    def init_oi_array(self,K=10):
        #find the spot price
        df=self.cur_option_chain
        df=df[df.expiryDate==self.expiry_date]
        self.spot_price=df.iloc[0]['PE.underlyingValue']





        cur_strike_price=int((self.spot_price+(self.delta/2))/self.delta)*self.delta

        self.base_strike_prices=self.cur_option_chain.strikePrice
        self.base_strike_prices.reset_index(drop=True,inplace=True)
        spot_idx=self.base_strike_prices[self.base_strike_prices==cur_strike_price].index[0]

        self.base_strike_prices=self.base_strike_prices[spot_idx-K:spot_idx+K]

        ce_oi=self.cur_option_chain["CE.openInterest"].to_numpy()
        pe_oi=self.cur_option_chain["PE.openInterest"].to_numpy()
        self.ce_ois=ce_oi[spot_idx-K:spot_idx+K].reshape(1,-1)
        self.pe_ois=pe_oi[spot_idx-K:spot_idx+K].reshape(1,-1)

        self.ce_sums=np.convolve(self.ce_ois[0],np.ones((self.num_sum,))).reshape(1,-1)
        self.pe_sums=np.convolve(self.pe_ois[0],np.ones((self.num_sum,))).reshape(1,-1)

        self.time_list=[datetime.now()]
        
        cur_spot_price=self.cur_option_chain.iloc[0]['PE.underlyingValue']
        self.spot_price_list=pd.DataFrame({'time':[datetime.now()],"price":[cur_spot_price]})
        
        self.time_list=[datetime.now(timezone("Asia/Kolkata"))]


    def open_interest_update_all(self,):
        temp_oc=self.cur_option_chain[self.cur_option_chain.strikePrice.isin(self.base_strike_prices)]
        
        ce_oi=temp_oc["CE.openInterest"].to_numpy()#+np.random.randint(10000)
        pe_oi=temp_oc["PE.openInterest"].to_numpy()


        self.ce_ois=np.append(self.ce_ois,ce_oi.reshape(1,-1),axis=0)
        self.pe_ois=np.append(self.pe_ois,pe_oi.reshape(1,-1),axis=0)

        ce_sum=np.convolve(ce_oi,np.ones((self.num_sum,)))        
        pe_sum=np.convolve(pe_oi,np.ones((self.num_sum,)))        
        #np.convolve(ce_prices[0],np.ones(5,))
        self.ce_sums=np.append(self.ce_sums,ce_sum.reshape(1,-1),axis=0)
        self.pe_sums=np.append(self.pe_sums,pe_sum.reshape(1,-1),axis=0)
        self.time_list.append(datetime.now(timezone("Asia/Kolkata")))

        cur_spot_price=self.cur_option_chain.iloc[0]['PE.underlyingValue']
        row=pd.DataFrame({'time':[datetime.now()],"price":[cur_spot_price]})
        self.spot_price_list=self.spot_price_list._append(row,ignore_index=False) 
            


def run_infinite():

    """
    strike_price_path=directory+"/data/strike_price.csv"
    ce_oi_data_path=directory+"/data/ce_oi_data.npy"
    pe_oi_data_path=directory+"/data/pe_oi_data.npy"
    ce_oi_data_sum_path=directory+"/data/ce_oi_data_sum.npy"
    pe_oi_data_sum_path=directory+"/data/pe_oi_data_sum.npy"
    spot_price=directory+"/data/spot_price.csv"
    """

    date=get_all_expiry_till_now(num_weeks_back=0)[0]

    expiry_date=formatted_date = date.strftime('%d-%b-%Y')


    #oc = OptionChain(symbol="NIFTY",timeout=5,expiry_date='24-Oct-2024',update_time=40,new_file=True)
    oc = OptionChain(symbol="NIFTY",timeout=5,expiry_date=expiry_date,update_time=40,new_file=True)
    #oc = OptionChain(symbol="NIFTY",timeout=5,expiry_date='22-Aug-2024',update_time=40,new_file=True)
    #filter time 
    while(True):
        oc.fetch_data()
        oc.open_interest_update_all()
        np.save(ce_oi_data_sum_path,oc.ce_sums)
        np.save(pe_oi_data_sum_path,oc.pe_sums)
        np.save(ce_oi_data_path,oc.ce_ois)
        np.save(pe_oi_data_path,oc.pe_ois)
        oc.base_strike_prices.to_csv(strike_price_path,index=False)
        oc.spot_price_list.to_csv(spot_price,index=False)
        
        #print(DBG)

        print("updated and saved..")
        time.sleep(5)






if __name__ == '__main__':
    #"""
    from option_chain import *
    #oc.display_new()
    """

    oc = OptionChain(symbol="NIFTY",timeout=5,expiry_date='30-May-2024',update_time=40)
    oc.display()
    """
    run_infinite()



