import datetime
import csv

# begin the unpack of the dividend history list!
with open('seed_data/amex_dividend_summary.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    prev_ticker_insurance = None
    for row in reader:
        ticker_insurance = row[7].strip()
        if ticker_insurance:
            prev_ticker_insurance = ticker_insurance
        else:
            ticker_insurance = prev_ticker_insurance
        dividendsummary = row[9].strip()
        if dividendsummary:
            dividendbroken = dividendsummary.split()
            if dividendbroken[0]!="Dividend":
                dividendtrimmed = dividendbroken[11:]
                for i in range(0,len(dividendtrimmed),6):
                    print ticker_insurance
                    effective_date = dividendtrimmed[i]
                    if effective_date:
                        effective_date = datetime.datetime.strptime(effective_date, "%m/%d/%Y")
                    else:
                        effective_date = None
                    print effective_date
                    dividend_type = dividendtrimmed[i+1]
                    print dividend_type
                    dividend_amount = dividendtrimmed[i+2]
                    print dividend_amount


        # good resource on how to get the items of a list unpacked
        # tickersymbol = row[6].rstrip()
        # if tickersymbol: 
        #     # print tickersymbol
        #     current_price = tickersymbol.split(" ")[1]
        #     # print current_price
