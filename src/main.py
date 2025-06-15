# main.py
import datetime
import time
import subprocess
import pytz


IST = pytz.timezone('Asia/Kolkata')

def is_market_open():
    now = datetime.datetime.now(IST)
    return(True)
    if now.weekday() >= 5:
        return False
        

    market_open = now.replace(hour=9, minute=15, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
    return market_open <= now <= market_close

def run_programs():
    # Start option_chain.py as background process
    option_chain = subprocess.Popen(["python3", "src/option_chain.py"])
    
    # Start Streamlit app
    streamlit = subprocess.Popen(["streamlit", "run", "src/display_oc.py", 
                                "--server.port=8501", "--server.address=0.0.0.0"])
    
    return option_chain, streamlit

def main():
    processes = None
    
    while True:
        current_time = datetime.datetime.now(IST).strftime("%H:%M:%S")
        
        if is_market_open() and not processes:
            print(f"{current_time} - Market OPEN - Starting programs")
            processes = run_programs()
            
        elif not is_market_open() and processes:
            print(f"{current_time} - Market CLOSED - Terminating programs")
            for p in processes:
                p.terminate()
            processes = None
            
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()



