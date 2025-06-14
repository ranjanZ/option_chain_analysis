import requests


def test_nse():
     symbol='NIFTY'
     url = "https://www.nseindia.com/api/option-chain-indices?symbol={}".format(symbol)
     session = requests.sessions.Session()
     session.headers = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5" }
     timeout = 5
     res=session.get("https://www.nseindia.com/option-chain", timeout=timeout)
     assert  res.status_code!=101


