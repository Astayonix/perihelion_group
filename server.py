"""Investing With The Perihelion Group"""

from jinja2 import StrictUndefined

from flask import Flask, request, render_template, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Stock, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/speculation', methods=['POST'])
def set_spec_pref():
    """Ask if the user wants to speculate."""
    # userpref = request.form.get("preference")
    userpref = True
    # userid = session.get("user_id")
    userid = 1

    user = User.query.get(userid)

    user.speculative = userpref
    db.session.commit()


    return "The user chose to speculate!"

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()