# -*- coding: utf-8 -*-
"""
@author: Karthik Iyer
"""
""" This script pulls in the last traded price of BTC from Bitfinex and 
    Kraken and sends an e-mail alert if a trading signal (entry/ exit) is 
    received.
"""
import time, json, requests, smtplib
FROMID = '' # A string of the form example@gmx.com
PASSWORD = '' # password associated with FROMID
TOID = '' # A string of the form example@gmail.com

# Helper functions
def bitfinex(): 
    # Get tick by tick data of last price from Bitfinex
    # https://www.bitfinex.com/pages/api
    bitFinexTick = requests.get("https://api.bitfinex.com/v1/ticker/btcusd")
    return bitFinexTick.json()['last_price']

def kraken():
     # Get tick by tick data of last price from Kraken
     # https://www.kraken.com/help/api
    krakenTick = requests.post('https://api.kraken.com/0/public/Ticker',
                               data=json.dumps({"pair":"XXBTZUSD"}),
        headers={"content-type":"application/json"})
    return krakenTick.json()['result']['XXBTZUSD']['c'][0]

def send_mail(fromid, toid, password, msg):
    # Send an e-mail alert
    server = smtplib.SMTP("smtp.gmx.com", 587 )
    server.starttls()
    server.login(FROMID, PASSWORD)
    server.sendmail(FROMID, [TOID], msg) #TOID is wrapped in a list

pos = None
while True:
    krakenUSDLive = float(kraken())
    bitfinexUSDLive = float(bitfinex())
    diff = bitfinexUSDLive - krakenUSDLive
   
    if pos is None: 
        if diff < -0.01*min(bitfinexUSDLive, krakenUSDLive):
            pos = 'Long'
            msg = '\n' + 'Potential BTC long spread: Bitifinex and Kraken.'
            msg = msg + '\n' + 'Long Bitifinex and short Kraken.' + "\n"
            send_mail(fromid=FROMID, toid=TOID, password=PASSWORD, 
                      msg=msg)
        
        if diff > 0.01*min(bitfinexUSDLive, krakenUSDLive):
            pos = 'Short'
            msg = '\n' + 'Potential BTC short spread: Bitifinex and Kraken.'
            msg = msg + '\n' + 'Short Bitifinex and long Kraken.' + "\n"
            send_mail(fromid=FROMID, toid=TOID, password=PASSWORD, 
                      msg=msg)
            
        if pos == 'Long' and diff >= 0.01*min(bitfinexUSDLive, krakenUSDLive):
            pos = None
            msg = '\n' + 'Close BTC long spread: Bitifinex and Kraken.'
            msg = msg + '\n' + 'Close the Bitfinex long and Kraken short.'+ "\n"
            send_mail(fromid=FROMID, toid=TOID, password=PASSWORD, 
                      msg=msg)
         
        if pos == 'Short' and diff <= -0.01*min(bitfinexUSDLive, krakenUSDLive):
            pos = None
            msg = '\n' + 'Close BTC short spread: Bitifinex and Kraken' 
            msg = msg + '\n' + 'Close the Bitfinex short and Kraken long.' + "\n"
            send_mail(fromid=FROMID, toid=TOID, password=PASSWORD, 
                      msg=msg)
       
    time.sleep(1800) # 1800 equals one hour. The API's are called every hour

