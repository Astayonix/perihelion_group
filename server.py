"""Investing With The Perihelion Group"""

from jinja2 import StrictUndefined

from flask import Flask, request, render_template, session, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Stock, Sector, Industry, connect_to_db, db


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

    print new_user
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
        stocks = Stock.query.offset(1).limit(20).all()
        user.stocks = stocks
        print user.stocks
        return render_template("portfoliomanager.html", userstocks=user.stocks)
    else:
        return redirect("/")


@app.route('/sectorselect')
def sectorselect():
    """Goes to the Sector Selection Page"""
    sectors = Sector.query.all()
    return render_template("sectorselect.html", sectors=sectors)

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
    companies = Stock.query.join(Industry).filter(Stock.industry_name.in_(industries)).all()
    return render_template("companyselect.html", companies=companies)

@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(user_name=username).first()
    print password
    print user.password
    print user.user_name

    if not user:
        flash("No such user")
        return redirect("/registrationtemplate")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/logintemplate")
    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/sectorselect")

# @app.route('/authenticate', methods=['POST'])
# def authenticate_user():
#     """Verify the user's name and password."""



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