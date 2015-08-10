# gdpdata = [240671000000, 267311000000, 327745000000, 375152000000, 518612000000, 541112000000, 632716000000, 746859000000, 896162000000, 1086198417793, 1197168102684]
# reversedgdpdata = reversed(gdpdata)

# def percentchange(currentyear, previousyear):
#     return ((float(currentyear)-previousyear)/abs(previousyear))*100.00

# for eachyear in reversedgdpdata:
#     deltagdp = percentchange(eachyear, gdpdata[0])
#     print eachyear, "||",deltagdp

import re
import csv
import itertools

seedfilelist = ['seed_data/amex_stock_summary.csv', 'seed_data/nasdaq_stock_summary.csv', 'seed_data/nyse_stock_summary.csv']

with open('seed_data/amex_stock_summary.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    for row in reader:
        # print list(itertools.chain(*reader))
        stockurl = row[5].rstrip()
        tickersymbol = row[6].rstrip()
        tickerinsurance = row[7].rstrip()
        companyname = row[8].rstrip()
        stocksummarydata = row[9].rstrip()

        re_one_yr_target = re.search(r"(Year Target )(-?\d+\.?\d+| NE | N\/A)", stocksummarydata)
        if re_one_yr_target:
            one_yr_target = re_one_yr_target.group(2)
        else:
            one_yr_target = None
        # print one_yr_target

        re_intra_day_high = re.search(r"(intra-day low. )(\$ )?(-?\d+\.?\d+| NE | N\/A)", stocksummarydata)
        if re_intra_day_high:
            intra_day_high = re_intra_day_high.group(3)
        else:
            intra_day_high = None
        # print intra_day_high

        re_intra_day_low = re.search(r"(intra-day low. )(\$ )?(-?\d+\.?\d+| NE | N\/A)?( / )(\$ )?(-?\d+\.?\d+| NE | N\/A)", stocksummarydata)
        if re_intra_day_low:
            intra_day_low = re_intra_day_low.group(6)
        else:
            intra_day_low = None
        # print intra_day_low

        companydesc = row[10].rstrip()
        print companydesc

        

# result = re.findall(r"t (\d+|NE|N\/A) T", stocksummarydata)
# print result

#(1 Year Target .* Today's High /Low "Today's High" The highest sales price the stock has achieved during the regular trading hours the intra-day high. "Today's Low" The lowest sales price the stock has fallen to during the regular trading hours the intra-day low.)?\d+