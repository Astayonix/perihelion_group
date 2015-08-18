import csv

# begin the unpack of the dividend history list!
with open('seed_data/amex_dividend_summary.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    for row in reader:
        dividendsummary = row[9].strip()
        if dividendsummary:
            dividendbroken = dividendsummary.split(" ")
            if dividendbroken[0]=="Dividend":
                pass
            else:
                print dividendbroken
        #     import pdb; pdb.set_trace()
            # disqualifer = "Dividend"
            # if dividendbroken[0] != disqualifier:
        #         for element in range(len(dividendbroken)/6):
        #            date, t, value = dividendbroken[11+element*6:14+element*6]
        #         print date


        # good resource on how to get the items of a list unpacked
        # tickersymbol = row[6].rstrip()
        # if tickersymbol: 
        #     # print tickersymbol
        #     current_price = tickersymbol.split(" ")[1]
        #     # print current_price
