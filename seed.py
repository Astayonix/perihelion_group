"""Utility file to seed ratings database from MovieLens data in seed_data/"""

import csv

# from model import User, Sector, Industry, Stock, StockQuoteSummary, StockUser, connect_to_db, db
from model import Sector, Industry, connect_to_db, db
# from model import Industry, connect_to_db, db
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
    # load_users()
    # load_movies()
    # load_ratings()
