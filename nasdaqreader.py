import csv

# begin the unpack of the companies available for trade on the amex, nasdaq, and nyse list!
# with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
#     reader = csv.reader(seedfile, delimiter=",")
#     reader.next()
#     uniquesectors = set()
#     for row in reader:
#         sectors = row[5].rstrip()
#         uniquesectors.add(sectors)
#     print uniquesectors

with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    uniqueindustries = set()
    for row in reader:
        industries = row[6].rstrip()
        uniqueindustries.add(industries)
    print uniqueindustries