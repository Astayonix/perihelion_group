"""Utility file to seed ratings database from MovieLens data in seed_data/"""

import re
import csv

from model import User, Sector, Industry, Stock, StockQuoteSummary, connect_to_db, db
from server import app


def load_sectors():
    """Load sectors from nasdaq.csv into the database."""

    print "Sectors"

    # begin the unpack of the companies available for trade on the amex, nasdaq, and nyse list!
    with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
        reader = csv.reader(seedfile, delimiter=",")
        reader.next()
        uniquesectors = set()
        for row in reader:
            sectors = row[5].rstrip()
            uniquesectors.add(sectors)
        for sectorname in uniquesectors:
            sector = Sector()
            sector.sector_name=sectorname
            db.session.add(sector)
    # Once we're done, we should commit our work
    db.session.commit()


def load_industries():
    """Load industries from nasdaq.csv into the database."""

    print "Industries"

    # begin the unpack of the companies available for trade on the amex, nasdaq, and nyse list!
    with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
        reader = csv.reader(seedfile, delimiter=",")
        reader.next()
        uniqueindustries = set()
        for row in reader:
            industries = row[6].rstrip()
            uniqueindustries.add(industries)
        for industryname in uniqueindustries:
            industry = Industry()
            industry.industry_name=industryname
            db.session.add(industry)
    # Once we're done, we should commit our work
    db.session.commit()


def load_stocks():
    """Load population of stocks from nasdaq.csv and into the database."""

    print "Create Stock Table"

    # all of the ticker symbols available for trade on the amex, nasdaq, and nyse list
    with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
        reader = csv.reader(seedfile, delimiter=",")
        for row in reader:
            # ticker, companyname, _, _, _, sector, industry, companyurl, _ = row
            # since row is an iterable, we can just go ahead and unpack the rows (underscore the values we're not interested in) 
            ticker = row[0]
            companyname = row[1]
            sector = row[5]
            industry = row[6]
            companyurl = row[7]
            stock = Stock(ticker_symbol=ticker,
                          company_name=companyname,
                          sector_name=sector,
                          industry_name=industry,
                          company_url=companyurl)

            db.session.add(stock)
    # Once we're done, we should commit our work
    db.session.commit()

def fill_stock_desc():
    """Load population of stocks from nasdaq.csv and into the database."""

    print "Fill Stock Desc"

    # all of the ticker symbols available for trade on the amex, nasdaq, and nyse list
    seedfilepathlist = ['seed_data/amex_stock_summary.csv', 'seed_data/nasdaq_stock_summary.csv', 'seed_data/nyse_stock_summary.csv']

    for seedfilepath in seedfilepathlist:

        with open(seedfilepath, 'rb') as seedfile:
            reader = csv.reader(seedfile, delimiter=",")
            reader.next()
            for row in reader:
                ticker = row[0]
                companyname = row[1]
                ticker = row[7]
                companydescription = row[10].decode("latin-1")
                stock = Stock.query.get(ticker)
                if stock:
                    stock.company_desc = companydescription

    # Once we're done, we should commit our work
    db.session.commit()


def load_stock_summary():
    """Load population of stocks summary information from nasdaq.csv and into the database."""

    print "Create Stock Summary Table"

    # all of the stock summary information available for the amex, nasdaq, and nyse list
    seedfilepathlist = ['seed_data/amex_stock_summary.csv', 'seed_data/nasdaq_stock_summary.csv', 'seed_data/nyse_stock_summary.csv']

    for seedfilepath in seedfilepathlist:

        with open(seedfilepath, 'rb') as seedfile:
            reader = csv.reader(seedfile, delimiter=",")
            reader.next()
            for row in reader:
                ticker = row[7]
                stocksummarydata = row[9]
                re_one_yr_target = re.search(r"(Year Target )(-?\d+\.?\d+|0)", stocksummarydata)
                if re_one_yr_target:
                    one_yr_target = re_one_yr_target.group(2)
                else:
                    one_yr_target = None
                re_intra_day_high = re.search(r"(intra-day low\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_intra_day_high:
                    intra_day_high = re_intra_day_high.group(3)
                else:
                    intra_day_high = None
                re_intra_day_low = re.search(r"(intra-day low\. )(\$ )?(-?\d+\.?\d+|0)?( / )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_intra_day_low:
                    intra_day_low = re_intra_day_low.group(6)
                else:
                    intra_day_low = None
                re_share_volume = re.search(r"(after hours volume\. )(-?\d+\.?\d+|0)", stocksummarydata)
                if re_share_volume:
                    share_volume = re_share_volume.group(2)
                else:
                    share_volume = None
                re_ninety_day_avg_volume = re.search(r"(average daily volume\. )(-?\d+\.?\d+|0)", stocksummarydata)
                if re_ninety_day_avg_volume:
                    ninety_day_avg_volume = re_ninety_day_avg_volume.group(2)
                else:
                    ninety_day_avg_volume = None
                re_previous_close = re.search(r"(official trading hours\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_previous_close:
                    previous_close = re_previous_close.group(3)
                else:
                    previous_close = None
                re_fifty_two_week_high = re.search(r"(most recent 52 week period\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_fifty_two_week_high:
                    fifty_two_week_high = re_fifty_two_week_high.group(3)
                else:
                    fifty_two_week_high = None
                re_fifty_two_week_low = re.search(r"(most recent 52 week period\. )(\$ )?(-?\d+\.?\d+|0)?( / )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_fifty_two_week_low:
                    fifty_two_week_low = re_fifty_two_week_low.group(6)
                else:
                    fifty_two_week_low = None
                re_market_cap = re.search(r"(the listing requirements\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_market_cap:
                    market_cap = re_market_cap.group(3)
                else:
                    market_cap = None
                re_pe_ratio = re.search(r"(the \"multiple\"\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_pe_ratio:
                    pe_ratio = re_pe_ratio.group(3)
                else:
                    pe_ratio = None
                re_forward_pe_one_yr = re.search(r"(value for the next full year\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_forward_pe_one_yr:
                    forward_pe_one_yr = re_forward_pe_one_yr.group(3)
                else:
                    forward_pe_one_yr = None
                re_earnings_per_share = re.search(r"(this is EBITDA EPS\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_earnings_per_share:
                    earnings_per_share = re_earnings_per_share.group(3)
                else:
                    earnings_per_share = None
                re_annualized_dividend = re.search(r"(Annualized dividend )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_annualized_dividend:
                    annualized_dividend = re_annualized_dividend.group(3)
                else:
                    annualized_dividend = None
                re_expected_dividend_date = re.search(r"(Ex Dividend Date )([A-Z]{1}[a-z]{2}\. [0-9]{2} [0-9]{4})", stocksummarydata)
                if re_expected_dividend_date:
                    expected_dividend_date = re_expected_dividend_date.group(2)
                else:
                    expected_dividend_date = None
                re_dividend_payment_date = re.search(r"(Dividend Payment Date )([A-Z]{1}[a-z]{2}\. [0-9]{2} [0-9]{4})", stocksummarydata)
                if re_dividend_payment_date:
                    dividend_payment_date = re_dividend_payment_date.group(2)
                else:
                    dividend_payment_date = None
                re_current_yield = re.search(r"(divided by current stock price\. )(\$ )?(-?\d+\.?\d?|0)", stocksummarydata)
                if re_current_yield:
                    current_yield = re_current_yield.group(3)
                else:
                    current_yield = None
                re_beta = re.search(r"(will rise or fall less\. )(\$ )?(-?\d+\.?\d+|0)", stocksummarydata)
                if re_beta:
                    beta = re_beta.group(3)
                else:
                    beta = None

                stocksummary = StockQuoteSummary(ticker_symbol=ticker,
                                one_yr_target=one_yr_target,
                                intra_day_high=intra_day_high,
                                intra_day_low=intra_day_low,
                                share_volume=share_volume,
                                ninety_day_avg_volume=ninety_day_avg_volume,
                                previous_close=previous_close,
                                fifty_two_week_high=fifty_two_week_high,
                                fifty_two_week_low=fifty_two_week_low,
                                market_cap=market_cap,
                                pe_ratio=pe_ratio,
                                forward_pe_one_yr=forward_pe_one_yr,
                                earnings_per_share=earnings_per_share,
                                annualized_dividend=annualized_dividend,
                                expected_dividend_date=expected_dividend_date,
                                dividend_payment_date=dividend_payment_date,
                                current_yield=current_yield,
                                beta=beta)

                db.session.add(stocksummary)
    # Once we're done, we should commit our work
    db.session.commit()

def fill_last_trade():
    """Load population of last trades from nasdaq.csv and into the database."""

    print "Fill Last Trade"

    # all of the ticker symbols available for trade on the amex, nasdaq, and nyse list
    with open('seed_data/amex_nasdaq_nyse_companies.csv', 'rb') as seedfile:
        reader = csv.reader(seedfile, delimiter=",")
        reader.next()
        for row in reader:
            ticker = row[0]
            last_trade = row[2]
            stock = StockQuoteSummary.query.filter_by(ticker_symbol=ticker).first()
            if stock:
                stock.last_trade = last_trade

    # # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    for i, row in enumerate(open("seed_data/u.item")):
        row = row.rstrip()

        # clever -- we can unpack part of the row!
        movie_id, title, released_str, junk, imdb_url = row.split("|")[:5]

        # The date is in the file as daynum-month_abbreviation-year;
        # we need to convert it to an actual datetime object.

        if released_str:
            released_at = datetime.datetime.strptime(released_str, "%d-%b-%Y")
        else:
            released_at = None

        # Remove the (YEAR) from the end of the title.

        title = title[:-7]   # " (YEAR)" == 7

        movie = Movie(movie_id=movie_id,
                      title=title,
                      released_at=released_at,
                      imdb_url=imdb_url)

        # We need to add to the session or it won't ever be stored
        db.session.add(movie)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    for i, row in enumerate(open("seed_data/u.data")):
        row = row.rstrip()

        user_id, movie_id, score, timestamp = row.split("\t")

        user_id = int(user_id)
        movie_id = int(movie_id)
        score = int(score)

        # We don't care about the timestamp, so we'll ignore this

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(rating)

        # provide some sense of progress
        if i % 1000 == 0:
            print i

            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.

            db.session.commit()

    # Once we're done, we should commit our work
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_sectors()
    load_industries()
    load_stocks()
    fill_stock_desc()
    load_stock_summary()
    fill_last_trade()
    # load_users()
    # load_movies()
    # load_ratings()
