"""Models and database functions for perihelion_group project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of the Perihelion Group's website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True) #auto-generated
    user_name = db.Column(db.String(100), nullable=False) #user provides
    password = db.Column(db.String(64), nullable=False) #user provides
    initial_investment = db.Column(db.Integer, nullable=True) #user provides
    speculative = db.Column(db.String(5), nullable=True)#user provides

    stocks = db.relationship('Stock', secondary="stockusers",
        backref=db.backref('users', lazy='dynamic'))
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User_id %s's name is %s>" % (self.user_id, self.user_name)


class Sector(db.Model):
    """A table containing all of the available sectors stocks can belong to."""

    __tablename__ = "sectors"

    sector_name = db.Column(db.String(100), primary_key=True) #seeded from nasdaq.csv
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<The sector is %s>" % (self.sector_name)

    def json(self):
        """Makes an dictionary representation of the StockUser"""
        jsonsector={}
        jsonsector["name"]=self.sector_name

        return jsonsector


class Industry(db.Model):
    """A table containing all of the available industries stocks can belong to."""

    __tablename__ = "industries"

    industry_name = db.Column(db.String(100), primary_key=True) #seeded from nasdaq.csv
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<The industry is %s>" % (self.industry_name)

    def json(self):
        """Makes an dictionary representation of the StockUser"""
        jsonindustry={}
        jsonindustry["name"]=self.industry_name
        
        return jsonindustry


class Stock(db.Model):
    """A list of all stocks available for investment on the Perihelion Group's website."""

    __tablename__ = "stocks"

    ticker_symbol = db.Column(db.String(15), primary_key=True) #seeded from nasdaq.csv (be sure to seed w/ " ")
    company_name = db.Column(db.String(200), nullable=False) #seeded from nasdaq.csv (be sure to seed w/ " ")
    sector_name = db.Column(db.String(100), db.ForeignKey('sectors.sector_name'), nullable=False)
    industry_name = db.Column(db.String(100), db.ForeignKey('industries.industry_name'), nullable=True)
    company_url = db.Column(db.String(50), nullable=False) #seeded from nasdaq.csv (be sure to seed w/ " ")
    company_desc = db.Column(db.Text, nullable=True) #seeded from stock_summary files
  
    sector = db.relationship('Sector', backref=db.backref('stocks'))
    industry = db.relationship('Industry', backref=db.backref('stocks'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<%s has a ticker symbol of %s, belongs to industry %s, and sector %s>" % (self.company_name, self.ticker_symbol, self.industry_name, self.sector_name)

    @classmethod
    def clusternester(cls,user_id):
        # import pdb; pdb.set_trace()
        sectors = {}
        for stock in cls.query.all():
            if stock.sector:
                currentindustries = sectors.get(stock.sector.sector_name, [])
                if stock.industry.industry_name not in currentindustries:
                    currentindustries.append(stock.industry.industry_name)
                sectors[stock.sector.sector_name]=currentindustries
        jsonsectors=[]
        dividendmax=None
        dividendmin=None
        # pdb.set_trace()
        for sector in sectors.keys():
            sectordict = {"name":sector, "children":[]}
            for industry in sectors[sector]:
                industrydict = {"name":industry, "children":[]}
                stockusers = StockUser.query.filter_by(user_id=user_id).all()
                for stockuser in stockusers:
                    if stockuser.stock.industry_name == industry:
                        industrydict["children"].append(stockuser.json())
                        if stockuser.stock.stockquotesummary[0].annualized_dividend > dividendmax:
                            dividendmax = stockuser.stock.stockquotesummary[0].annualized_dividend
                        elif stockuser.stock.stockquotesummary[0].annualized_dividend < dividendmin or dividendmin == None:
                            dividendmin = stockuser.stock.stockquotesummary[0].annualized_dividend

                sectordict["children"].append(industrydict)
            jsonsectors.append(sectordict)
        dividendmid = (dividendmax + dividendmin) / 2
        alldividenddata = {"children":jsonsectors, "name": "Economy", "min":dividendmin, "max":dividendmax, "mid":dividendmid}
        # import pdb; pdb.set_trace()
        return alldividenddata


class StockQuoteSummary(db.Model):
    """The summary snapshoot of all stock activity on the Perihelion Group's website."""

    __tablename__ = "stockquotesummary"

    stock_summary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ticker_symbol = db.Column(db.String(15), db.ForeignKey('stocks.ticker_symbol'), unique=True, nullable=False)
    # ticker_quote_summary = db.Column(db.String(500), nullable=False) #needs to be unpacked becuase produces multiple columns
    # stock_summary_data = db.Column(db.String(1000), nullable=False) #needs to be unpacked becuase produces multiple columns
    last_trade  = db.Column(db.Integer, nullable=True) #seeded from nasdaq.csv (seed initially with " ")
    one_yr_target = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    intra_day_high = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    intra_day_low = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    share_volume = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    ninety_day_avg_volume = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    previous_close = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    fifty_two_week_high = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    fifty_two_week_low = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    market_cap = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    pe_ratio = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    forward_pe_one_yr = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    earnings_per_share = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    annualized_dividend = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    expected_dividend_date = db.Column(db.String(20), nullable=True) #seeded from the stock_summary files
    dividend_payment_date = db.Column(db.String(20), nullable=True) #seeded from the stock_summary files
    current_yield = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files
    beta = db.Column(db.Integer, nullable=True) #seeded from the stock_summary files

    stock = db.relationship('Stock', backref=db.backref('stockquotesummary'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<%s belongs to %s.>" % (self.stock_summary_id, self.ticker_symbol)


class DividendSummary(db.Model):
#     """The dividend activity for all the stocks available on the Perihelion Group's website."""

    __tablename__ = "stockdividends"

    dividend_summary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ticker_symbol = db.Column(db.String(15), db.ForeignKey('stocks.ticker_symbol'), unique=False, nullable=False)
    # dividend_summary_data = db.Column(db.String(1000), nullable=False) #needs to be unpacked becuase produces multiple columns
    effective_date = db.Column(db.DateTime, unique=False, nullable=False)
    dividend_type = db.Column(db.Integer, unique=False, nullable =False)
    dividend_amount = db.Column(db.Integer, unique=False, nullable=False)
   
    stock = db.relationship('Stock', backref=db.backref('stockdividends'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<%s's dividend summary info belongs to %s>" % (self.dividend_summary_id, self.ticker_symbol)


# class IncomeStatementSummary(db.Model):
#     """The income statement summary activity for all the stocks available on the Perihelion Group's website."""

#     __tablename__ = "stockincomestatements"

#     income_statement_summary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     ticker_symbol = db.Column(db.String(15), db.ForeignKey('stocks.ticker_symbol'), nullable=False)
#     income_statement_summary_data = db.Column(db.String(1000), nullable=False) #needs to be unpacked becuase produces multiple columns
    
#     ticker_symbol = db.relationship('Stocklist', backref=db.backref('stock_income_statements'))

# #     def __repr__(self):
# #         """Provide helpful representation when printed."""

# #         return "<%s's income statement summary info belongs to %s>" % (self.income_statement_summary_id, self.ticker_symbol)


class StockUser(db.Model):
    """Stock and User interaction on the Perihelion Group's website."""

    __tablename__ = "stockusers"

    stockuser_id = db.Column(db.Integer, autoincrement=True, primary_key=True) #auto generated
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    ticker_symbol = db.Column(db.String(15), db.ForeignKey('stocks.ticker_symbol'), nullable=False)

    user = db.relationship('User', backref=db.backref('stockusers'))
    stock = db.relationship('Stock', backref=db.backref('stockusers'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<%s is %s, who owns %s>" % (self.stockuser_id, self.user_id, self.ticker_symbol)

    def json(self):
        """Makes an dictionary representation of the StockUser"""
        jsonstockuser={}
        jsonstockuser["name"]=self.stock.company_name
        jsonstockuser["ticker"]=self.stock.ticker_symbol
        jsonstockuser["size"]=1
        jsonstockuser["dividend"]=self.stock.stockquotesummary[0].annualized_dividend
        # try:  
        #     jsonstockuser["size"]=self.stock.stockquotesummary[0].annualized_dividend
        # except:
        #     jsonstockuser["size"]=None
        return jsonstockuser

    def stockdetail(self):
        """Makes a dictionary representation of the Stock Details"""
        jsonstockdetail={}
        jsonstockdetail["dividend"]=self.stock.stockquotesummary[0].annualized_dividend
        jsonstockdetail["lasttrade"]=self.stock.stockquotesummary[0].last_trade
        jsonstockdetail["sharevolume"]=self.stock.stockquotesummary[0].share_volume
        jsonstockdetail["marketcap"]=self.stock.stockquotesummary[0].market_cap
        jsonstockdetail["peratio"]=self.stock.stockquotesummary[0].pe_ratio
        jsonstockdetail["eps"]=self.stock.stockquotesummary[0].earnings_per_share
        
        return jsonstockdetail

    def dividenddetail(self):
        """Makes a dictionary representation of the Dividend Details"""
        jsondividenddetail={}
        jsondividenddetail["dividenddate"]=self.stock.stockdividends.effective_date
        jsondividenddetail["dividendamount"]=self.stock.stockdividends.dividend_amount

        return jsondividenddetail


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///perihelion_group.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to The Perihelion Group's DB."