import csv

# begin the unpack of the dividend history list!
with open('seed_data/amex_dividend_summary.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    for row in reader:
        ticker_insurance = row[7].strip()
        print ticker_insurance
        dividendsummary = row[9].strip()
        if dividendsummary:
            dividendbroken = dividendsummary.split()
            if dividendbroken[0]!="Dividend":
                dividendtrimmed = dividendbroken[11:]
                for i in range(0,len(dividendtrimmed),6):
                    effective_date = dividendtrimmed[i]
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
