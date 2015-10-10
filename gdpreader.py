# dropping the GDP portion of the project in the interest of time.
import csv

with open('seed_data/global_gdp_data.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    uniquecountries = set()
    for row in reader:
        countryname = row[0].rstrip()
        uniquecountries.add(countryname)

    # uniquesegment = set()
    # for row in reader:
    #     # print row[2].rstrip()
    #     economicsegment = row[2].rstrip()
    #     uniquesegment.add(economicsegment)
    # print economicsegment

# gdpdata = [240671000000, 267311000000, 327745000000, 375152000000, 518612000000, 541112000000, 632716000000, 746859000000, 896162000000, 1086198417793, 1197168102684]
# reversedgdpdata = reversed(gdpdata)

# def percentchange(currentyear, previousyear):
#     return ((float(currentyear)-previousyear)/abs(previousyear))*100.00

# for eachyear in reversedgdpdata:
#     deltagdp = percentchange(eachyear, gdpdata[0])
#     print eachyear, "||",deltagdp
