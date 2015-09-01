"""Investing With The Perihelion Group"""

from jinja2 import StrictUndefined

from flask import Flask, request, render_template, session, flash, redirect, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from sqlalchemy import or_, and_

from model import User, Stock, Sector, Industry, StockUser, StockQuoteSummary, DividendSummary, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC123"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("index.html")

@app.route('/registrationtemplate')
def registrationtemplate():
    """Registration Page."""

    return render_template("registration.html")

@app.route('/registration', methods=['POST'])
def user_registration():
    """Create a Perihelion Group User."""
    username = request.form["username"]
    password = request.form["password"]
    investment = int(request.form["investment"]) 
    speculative = request.form["speculative"]

    new_user = User(user_name=username, password=password, initial_investment=investment, speculative=speculative)

    db.session.add(new_user)
    db.session.commit()

    flash("%s, Welcome to the Perihelion Group!" % username)
    return redirect("/logintemplate")

@app.route('/logintemplate')
def logintemplate():
    """Goes to the Login Page."""

    return render_template("login.html")

@app.route('/portfoliomanagertemplate')
def portfoliotemplate():
    """Goes to the Portfolio Manager Page."""
    current_user_id = session.get('user_id')


    if current_user_id:
        user = User.query.filter_by(user_id=current_user_id).one()
        selected_stocktickers = request.args.getlist('companies')
        individual_stocks = []

        for stock_ticker in selected_stocktickers:

            stock = Stock.query.get(stock_ticker)
            individual_stocks.append(stock)

        user.stocks.extend(individual_stocks)
        db.session.commit()

        return render_template("portfoliomanager.html", userstocks=user.stocks)
    else:
        return redirect("/")


@app.route('/sectorselect')
def sectorselect():
    """Goes to the Sector Selection Page"""

    # already_selected_sector = User.query.join(Stock).join(Sector).filter(user_name=username).first()
    current_user_ticker_list = db.session.query(StockUser.ticker_symbol).filter_by(user_id=session["user_id"]).all()

    current_user_tickers = [ticker_tuple[0] for ticker_tuple in current_user_ticker_list]

    print "This is a test.", current_user_tickers

    sectors = db.session.query(Stock.sector_name).filter(~Stock.ticker_symbol.in_(current_user_tickers)).all()

    list_of_sectors = [sector_tuple[0] for sector_tuple in sectors]

    unique_sectors = set(list_of_sectors)

    # for sector in sectors:
    #     if already_selected_sector not in sectors:
    #     return sectors

    return render_template("sectorselect.html", sectors=unique_sectors)


@app.route('/industryselect')
def industryselect():
    """Goes to the Industry Selection Page"""
    sectors = request.args.getlist("sectors")
    industries = Industry.query.join(Stock).filter(Stock.sector_name.in_(sectors)).all()
    return render_template("industryselect.html", industries=industries)


@app.route('/companyselect')
def companyselect():
    """Goes to the Company Selection Page"""
    industries = request.args.getlist("industries")
    tickers_set = set()
    companies = Stock.query.join(Industry).filter(Stock.industry_name.in_(industries)).all()
    current_user_id = session.get('user_id')
    user = User.query.filter_by(user_id=current_user_id).first()

    if user.speculative == "No":
        print "is not speculative", user.speculative
        for company in companies: 
            for c in company.stockdividends:
                tickers_set.add(c.ticker_symbol)
    else:
        print "is speculative", user.speculative
        for company in companies:
            tickers_set.add(company.ticker_symbol)

    return render_template("companyselect.html", companies=companies)

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(user_name=username).first()

    if not user:
        flash("No such user")
        return redirect("/registrationtemplate")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/logintemplate")
    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/sectorselect")

@app.route('/portfoliojson', methods=['GET'])
def portfolio_json():
    """JSONify the user's stock portfolio."""
    # alluserstocks = StockUser.query.filter_by(user_id=session.get("user_id")).all()
    # jsonlist=[]
    # for userstock in alluserstocks:
    #     jsonlist.append(userstock.json())
    # data = {"children":jsonlist,"name":"stockidentifier"}
    # print data
    # import pdb;pdb.set_trace()
    data=Stock.clusternester(session.get("user_id"))
    outerdata = {"children": data, "name": "stockidentifier"}
    return jsonify(outerdata)




#     user_name = 
#     password = 
#     initial_investment = 
#     speculative =

#     new_user = User(email=email, password=password, age=age, zipcode=zipcode)

#     db.session.add(new_user)
#     db.session.commit()

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()