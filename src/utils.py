import pandas as pd
import numpy as np 


strike_price_path="data/strike_price.csv"
spot_price_path="data/spot_price.csv"
ce_oi_data_path="data/ce_oi_data.npy"
pe_oi_data_path="data/pe_oi_data.npy"
ce_oi_data_sum_path="data/ce_oi_data_sum.npy"
pe_oi_data_sum_path="data/pe_oi_data_sum.npy"

spot_price="data/spot_price.csv"



def get_market_direction_data(pe_strike_price,ce_strike_price,num_sum=5):
    try:
        ce_sums=np.load(ce_oi_data_sum_path,allow_pickle=True) 
        pe_sums=np.load(pe_oi_data_sum_path,allow_pickle=True)    
        base_strike_prices=pd.read_csv(strike_price_path)    
    
        ce_idx=base_strike_prices.loc[base_strike_prices['strikePrice']==ce_strike_price].index[0]
        pe_idx=base_strike_prices.loc[base_strike_prices['strikePrice']==pe_strike_price].index[0]
    
        pe_idx=ce_idx+num_sum-1
        
        d1_diff=(pe_sums[:,pe_idx]-ce_sums[:,ce_idx])/100000
        #print(pe_idx,ce_idx,base_strike_prices,d1_diff,pe_sums[:,pe_idx],ce_sums[:,ce_idx])
        #print(pe_strike_price,ce_strike_price)


    except:
        d1_diff=np.array([])
    return(d1_diff)





def get_spot_price():
    df=pd.read_csv(spot_price_path)    
    return(df)

def get_strike_prices():
    df=pd.read_csv(strike_price_path)    
    sp=df['strikePrice'].to_list()

    return(sp)








#################################compute all expiry################

from datetime import datetime, timedelta

# List of holidays in datetime format
holidays = [
    datetime(2025, 2, 26),  # Mahashivratri
    datetime(2025, 3, 14),  # Holi
    datetime(2025, 3, 31),  # Id-Ul-Fitr (Ramadan Eid)
    datetime(2025, 4, 10),  # Shri Mahavir Jayanti
    datetime(2025, 4, 14),  # Dr. Baba Saheb Ambedkar Jayanti
    datetime(2025, 4, 18),  # Good Friday
    datetime(2025, 5, 1),   # Maharashtra Day
    datetime(2025, 8, 15),  # Independence Day / Parsi New Year
    datetime(2025, 8, 27),  # Shri Ganesh Chaturthi
    datetime(2025, 10, 2),  # Mahatma Gandhi Jayanti/Dussehra
    datetime(2025, 10, 21), # Diwali Laxmi Pujan
    datetime(2025, 10, 22), # Balipratipada
    datetime(2025, 11, 5),  # Prakash Gurpurb Sri Guru Nanak Dev
    datetime(2025, 12, 25)  # Christmas
]

def is_holiday(date):
    """Check if the given date is a holiday."""
    return date in holidays

def get_previous_working_day(date):
    """Get the previous working day if the given date is a holiday."""
    while is_holiday(date) or date.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
        date -= timedelta(days=1)
    return date

def generate_weekly_expiry_dates(year, expiry_day=3):
    """
    Generate weekly expiry dates for Nifty in the given year.
    expiry_day: 0 = Monday, 1 = Tuesday, ..., 6 = Sunday (default is 3 for Thursday).
    """
    expiry_dates = []
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    current_date = start_date
    while current_date <= end_date:
        # Check if the current date is the specified expiry day
        if current_date.weekday() == expiry_day:
            expiry_date = current_date
            if is_holiday(expiry_date):
                expiry_date = get_previous_working_day(expiry_date)
            expiry_dates.append(expiry_date)
        current_date += timedelta(days=1)

    return expiry_dates

def get_next_expiry(input_date, expiry_day=3):
    """
    Get the next expiry date for Nifty given an input datetime.
    expiry_day: 0 = Monday, 1 = Tuesday, ..., 6 = Sunday (default is 3 for Thursday).
    """
    # Start from the input date to avoid returning the same day if it's already an expiry
    current_date = input_date

    while True:
        # Check if the current date is the specified expiry day
        if current_date.weekday() == expiry_day:
            expiry_date = current_date
            if is_holiday(expiry_date):
                expiry_date = get_previous_working_day(expiry_date)
            expiry_date = expiry_date.replace(hour=15, minute=30, second=0, microsecond=0)
            return expiry_date
        current_date += timedelta(days=1)




def get_all_expiry_till_now(num_weeks_back=3):
    weekly_expiry_dates_2025 = generate_weekly_expiry_dates(2025,)
    start_time=datetime.now()-timedelta(weeks=num_weeks_back)
    end_time=datetime.now()+timedelta(weeks=1)
    expiry_list=[]

    for i in range(len(weekly_expiry_dates_2025)):
        exp=weekly_expiry_dates_2025[i]
        if(exp<=end_time and exp>start_time):
            expiry_list.append(exp)

    return(expiry_list)


