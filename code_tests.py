# gdpdata = [240671000000, 267311000000, 327745000000, 375152000000, 518612000000, 541112000000, 632716000000, 746859000000, 896162000000, 1086198417793, 1197168102684]
# reversedgdpdata = reversed(gdpdata)

# def percentchange(currentyear, previousyear):
#     return ((float(currentyear)-previousyear)/abs(previousyear))*100.00

# for eachyear in reversedgdpdata:
#     deltagdp = percentchange(eachyear, gdpdata[0])
#     print eachyear, "||",deltagdp

import re
import csv
import datetime

# seedfilelist = ['seed_data/amex_stock_summary.csv', 'seed_data/nasdaq_stock_summary.csv', 'seed_data/nyse_stock_summary.csv']

with open('seed_data/amex_stock_summary.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    for row in reader:
        
        companyname = row[8].rstrip(" Stock Quote & Summary Data")
        if not companyname:
            continue
        # print companyname #done

        stockurl = row[5].rstrip()
        # print stockurl #done
 
        # good resource on how to get the items of a list unpacked
        # tickersymbol = row[6].rstrip()
        # if tickersymbol: 
        #     # print tickersymbol
        #     current_price = tickersymbol.split(" ")[1]
        #     # print current_price
        
        tickerinsurance = row[7].rstrip()
        # print tickerinsurance #done
        
        stocksummarydata = row[9].rstrip()

        re_one_yr_target = re.search(r"(Year Target )(-?\d+\.?\d+|0)", stocksummarydata)
        if re_one_yr_target:
            one_yr_target = re_one_yr_target.group(2)
        else:
            one_yr_target = None
        # print one_yr_target #done

        re_intra_day_high = re.search(r"(intra-day low\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_intra_day_high:
            intra_day_high = re_intra_day_high.group(3)
        else:
            intra_day_high = None
        # print intra_day_high #done

        re_intra_day_low = re.search(r"(intra-day low\. )(\$ )?(-?\d+\.?\d+|0)?( / )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_intra_day_low:
            intra_day_low = re_intra_day_low.group(6)
        else:
            intra_day_low = None
        # print intra_day_low #done

        re_share_volume = re.search(r"(after hours volume\. )(-?\d+\.?\d+|0)", stocksummarydata)
        if re_share_volume:
            share_volume = re_share_volume.group(2)
        else:
            share_volume = None
        # print share_volume #done

        re_ninety_day_avg_volume = re.search(r"(average daily volume\. )(-?\d+\.?\d+|0)", stocksummarydata)
        if re_ninety_day_avg_volume:
            ninety_day_avg_volume = re_ninety_day_avg_volume.group(2)
        else:
            ninety_day_avg_volume = None
        # print ninety_day_avg_volume #done

        re_previous_close = re.search(r"(official trading hours\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_previous_close:
            previous_close = re_previous_close.group(3)
        else:
            previous_close = None
        # print previous_close #done

        re_fifty_two_week_high = re.search(r"(most recent 52 week period\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_fifty_two_week_high:
            fifty_two_week_high = re_fifty_two_week_high.group(3)
        else:
            fifty_two_week_high = None
        # print fifty_two_week_high #done

        re_fifty_two_week_low = re.search(r"(most recent 52 week period\. )(\$ )?(-?\d+\.?\d+|0)?( / )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_fifty_two_week_low:
            fifty_two_week_low = re_fifty_two_week_low.group(6)
        else:
            fifty_two_week_low = None
        # print fifty_two_week_low #done

        re_market_cap = re.search(r"(the listing requirements\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_market_cap:
            market_cap = re_market_cap.group(3)
        else:
            market_cap = None
        # print market_cap #done

        re_pe_ratio = re.search(r"(the \"multiple\"\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_pe_ratio:
            pe_ratio = re_pe_ratio.group(3)
        else:
            pe_ratio = None
        # print pe_ratio #done

        re_forward_pe_one_yr = re.search(r"(value for the next full year\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_forward_pe_one_yr:
            forward_pe_one_yr = re_forward_pe_one_yr.group(3)
        else:
            forward_pe_one_yr = None
        # print forward_pe_one_yr #done

        re_earnings_per_share = re.search(r"(this is EBITDA EPS\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_earnings_per_share:
            earnings_per_share = re_earnings_per_share.group(3)
        else:
            earnings_per_share = None
        # print earnings_per_share #done

        re_annualized_dividend = re.search(r"(Annualized dividend )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_annualized_dividend:
            annualized_dividend = re_annualized_dividend.group(3)
        else:
            annualized_dividend = None
        # print annualized_dividend #done

        re_expected_dividend_date = re.search(r"(Ex Dividend Date )([A-Z]{1}[a-z]{2}\. [0-9]{2} [0-9]{4})", stocksummarydata)
        if re_expected_dividend_date:
            expected_dividend_date = re_expected_dividend_date.group(2)
        else:
            expected_dividend_date = None
        # print expected_dividend_date #done
        
        re_dividend_payment_date = re.search(r"(Dividend Payment Date )([A-Z]{1}[a-z]{2}\. [0-9]{2} [0-9]{4})", stocksummarydata)
        if re_dividend_payment_date:
            dividend_payment_date = re_dividend_payment_date.group(2)
        else:
            dividend_payment_date = None
        # print dividend_payment_date #done

        re_current_yield = re.search(r"(divided by current stock price\. )(\$ )?(-?\d+\.?\d?|0)", stocksummarydata)
        if re_current_yield:
            current_yield = re_current_yield.group(3)
        else:
            current_yield = None
        # print current_yield #done

        re_beta = re.search(r"(will rise or fall less\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
        if re_beta:
            beta = re_beta.group(3)
        else:
            beta = None
        # print beta #done

        re_companydesc = row[10].rstrip()
        if re_companydesc:
            companydesc = re_companydesc
        else:
            companydesc = None
        # print companydesc        

# begin the unpack of the dividend history list!
with open('seed_data/amex_dividend_summary.csv', 'rb') as seedfile:
    reader = csv.reader(seedfile, delimiter=",")
    reader.next()
    for row in reader:
        dividendsummary = row[9].strip()
        disqualifer = "Dividend"
        if dividendsummary:
            dividendbroken = dividendsummary.split(" ")
            import pdb; pdb.set_trace()
            if dividendbroken[0] != disqualifier:
                for element in range(len(dividendbroken)/6):
                   date, t, value = dividendbroken[11+element*6:14+element*6]


        # good resource on how to get the items of a list unpacked
        # tickersymbol = row[6].rstrip()
        # if tickersymbol: 
        #     # print tickersymbol
        #     current_price = tickersymbol.split(" ")[1]
        #     # print current_price

# result = re.findall(r"t (\d+|NE|N\/A) T", stocksummarydata)
# print result

#(1 Year Target .* Today's High /Low "Today's High" The highest sales price the stock has achieved during the regular trading hours the intra-day high. "Today's Low" The lowest sales price the stock has fallen to during the regular trading hours the intra-day low.)?\d+