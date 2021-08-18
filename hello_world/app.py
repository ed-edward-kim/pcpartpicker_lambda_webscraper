import json
import requests
import smtplib, ssl #For emailing. Gmail SMTP server and ssl for encryption
import sys #for dealing with command line arguments sys.argv
import csv #for file io. reading in list separated by commas of products we want to check.
from datetime import datetime #for telling date and time for email
import time #for refresh intervals.
import getpass #to hide password when typing it in

from bs4 import BeautifulSoup #Beautiful soup for formatting HTML things

port = 465 #For SSL
ssl_context = ssl.create_default_context() #create secure SSL context
message = """\
Subject: %s has dropped below your set price of $%s

Product: %s
Current price of this product: $%s
See product at: %s
Message sent at: %s. UTC
This message is sent from python. 

"""
def lambda_handler(event, context):
    sender = 'Put_Your_Email_Here'
    password = 'Put_Your_Password_Here'
    
    print("Logging in please wait...")

    login = False #checking if user and pass are valid
    while login == False:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ssl_context) as server:
            try:
                server.login(sender, password)
                print("Log in successful!")
                login = True
            except:
                raise Exception
                
    receiver = sender

    try:
        filename= 'products.csv' #argv[0]
        print("opening ", filename, "...")
        
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            print("Begin test")
            for row in csv_reader: #row[0] is product name, row[1] holds price to be for buying, row[2] is the link
                product_name = row[0]
                wanted_price = float(row[1])
                URL = row[2]

                try:
                    page = requests.get(URL)
                    soup = BeautifulSoup(page.content, "html.parser")
                    results = soup.find(id="product-page")
                    title_element = results.find("h1", class_="pageTitle") #gets title of product...
                    price_element = results.find("td", class_="td__base") #does 1 find for the first merchant as pcpartpicker automatically sorts lowest price first!
                except Exception as err:
                    print("DDos protection stopped this application from scrapping the product, or PcPartPicker changed their HTML...")
                    raise err

                price = float(price_element.text[1:]) #[1:] to remove the dollar sign to set up for comparing...
                if price_element == None: #edge case for checking if price exists. 
                    print(title_element.text)
                    print("No price found. Please check if listing was removed!")
                if price <= wanted_price:
                    now = datetime.utcnow()
                    timesent = now.strftime("%d/%m/%Y %H:%M:%S")
                    new_message = message % (product_name, wanted_price, product_name, price, URL, timesent)
                    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=ssl_context) as server:
                        server.login(sender, password)
                        server.sendmail(sender,receiver,new_message)
                    print("Neat!")
                else:
                    print("oof")
                    

    except Exception as err:
        print("Error")
        raise err
    return("Success! Please check emails for notifications...")
