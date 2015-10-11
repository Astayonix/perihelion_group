import csv

# all of the unique sectors available for trade on the amex, nasdaq, and nyse list
with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    uniquesectors = set()
    for row in reader:
        sectors = row[5].rstrip()
        uniquesectors.add(sectors)

# all of the unique industries available for trade on the amex, nasdaq, and nyse list
with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    uniqueindustries = set()
    for row in reader:
        industries = row[6].rstrip()
        uniqueindustries.add(industries)

# all of the ticker symbols available for trade on the amex, nasdaq, and nyse list
with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    for row in reader:
        tickersymbol = row[0].rstrip()

# all of the company names available for trade on the amex, nasdaq, and nyse list
with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    for row in reader:
        companyname = row[1].rstrip()

# all of the company urls available for trade on the amex, nasdaq, and nyse list
with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    for row in reader:
        companyurl = row[7].rstrip()

# last trading price of all the companies available for trade on the amex, nasdaq, and nyse list
with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    for row in reader:
        lasttradeprice = row[2].rstrip()