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

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    initial_investment = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User_id %s's name is %s>" % (self.user_id, self.user_name)


class Sector(db.Model):
    """A table containing all of the available sectors stocks can belong to."""

    __tablename__ = "sectors"

    sector_name = db.Column(db.String(100), primary_key=True)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Sector_id %s's name is %s>" % (self.sector_id, self.sector_name)


class Industry(db.Model):
    """A table containing all of the available industries stocks can belong to."""

    __tablename__ = "industries"

    industry_name = db.Column(db.String(100), primary_key=True)
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Industry_id %s's name is %s>" % (self.industry_id, self.industry_name)


class StockList(db.Model):
    """A list of all stocks available for investment on the Perihelion Group's website."""

    __tablename__ = "stocks"

    ticker_symbol = db.Column(db.String(15), primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    sector_name = db.Column(db.String(100), db.ForeignKey('sectors.sector_name'), nullable=True)
    industry_name = db.Column(db.String(100), db.ForeignKey('industries.industry_name'), nullable=True)
    company_desc = db.Column(db.Text, nullable=True)

    sector_name = db.relationship('Sector', backref=db.backref('sectors'))
    industry_name = db.relationship('Industry', backref=db.backref('industries'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<%s has a ticker symbol of %s, belongs to industry %s, and sector %s>" % (self.company_name, self.ticker_symbol, self.industry_name, self.sector_name)


class StockQuoteSummary(db.Model):
    """The summary snapshoot of all stock activity on the Perihelion Group's website."""

    __tablename__ = "stockquotesummary"

    stock_summary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ticker_symbol = db.Column(db.String(15), db.ForeignKey('stocks.ticker_symbol'), nullable=False)
    ticker_quote_summary = db.Column(db.String(500), nullable=False) #needs to be unpacked becuase produces multiple columns
    stock_summary_data = db.Column(db.String(1000), nullable=False) #needs to be unpacked becuase produces multiple columns

    ticker_symbol = db.relationship('StockList', backref=db.backref('stock_quote_summaries'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<%s belongs to %s and has a dashboard summary of %s>" % (self.stock_summary_id, self.ticker_symbol, self.ticker_quote_summary)


class DividendSummary(db.Model):
    """The dividend activity for all the stocks available on the Perihelion Group's website."""

    __tablename__ = "stockdividends"

    dividend_summary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ticker_symbol = db.Column(db.String(15), db.ForeignKey('stocks.ticker_symbol'), nullable=False)
    dividend_summary_data = db.Column(db.String(1000), nullable=False) #needs to be unpacked becuase produces multiple columns
    
    ticker_symbol = db.relationship('StockList', backref=db.backref('stock_dividends'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<%s's dividend summary info belongs to %s>" % (self.dividend_summary_id, self.ticker_symbol)


class IncomeStatementSummary(db.Model):
    """The income statement summary activity for all the stocks available on the Perihelion Group's website."""

    __tablename__ = "stockincomestatements"

    income_statement_summary_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    ticker_symbol = db.Column(db.String(15), db.ForeignKey('stocks.ticker_symbol'), nullable=False)
    income_statement_summary_data = db.Column(db.String(1000), nullable=False) #needs to be unpacked becuase produces multiple columns
    
    ticker_symbol = db.relationship('Stocklist', backref=db.backref('stock_income_statements'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<%s's income statement summary info belongs to %s>" % (self.income_statement_summary_id, self.ticker_symbol)


class StockUser(db.Model):
    """Stock and User interaction on the Perihelion Group's website."""

    __tablename__ = "stockusers"

    stockuser_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))
    ticker_symbol = db.Column(db.String(15), db.ForeignKey('StockList.ticker_symbol'))

    user_id = db.relationship('User', backref=db.backref('stock_users'))
    ticker_symbol = db.relationship('StockList', backref=db.backref('stock_users'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<%s is %s, who owns %s>" % (self.stockuser_id, self.user_id, self.ticker_symbol)


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