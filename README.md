# The Perihelion Group
======================
An app based on the investment philosophy of The Perihelion Group

<h2>Overview</h2>
The Perihelion Group is a stock portfolio selection tool that allows the user to invest the same way I would if I ran a hedge fund. Driven on an investment philosophy emphasizing diversification and dividend yield, I scraped all stocks available for trade on the AMEX, NASDAQ, and NYSE exchanges. The resulting database is conducive to emphasizing dividend yield. Also collected were the GDP break-downs of every country on earth to create of a predictive model that takes into account which sectors of a nation’s economy are most likely to grow (available in v2.0). High dividend yield companies are paired with high-growth countries to allow the investor to ride a wave of success.

This is a visualization tool meant to help investors think more strategically about the kind of returns they want from their stock portfolios.  Using The Perihelion Group, investors can ask themselves questions like "Are my investments too heavily weighted in a specific sector and/or industry?" and "Is the dividend yield I am expecting aggressive enough to meet my liquid asset needs?"  I want to get people thinking differently about their data in a disruptive - yet intuitive - way.

<h5> Visualization of User Experience </h5>
Landing Page:
![alt tag](https://github.com/Astayonix/perihelion_group/blob/master/static/images/tpg_ux_1.jpg)

User Registration:
![alt tag](https://github.com/Astayonix/perihelion_group/blob/master/static/images/tpg_ux_2.jpg)

User Signs In:
![alt tag](https://github.com/Astayonix/perihelion_group/blob/master/static/images/tpg_ux_3.jpg)

User Selects Sectors:
![alt tag](https://github.com/Astayonix/perihelion_group/blob/master/static/images/tpg_ux_4.jpg)

User Selects Industries:
![alt tag](https://github.com/Astayonix/perihelion_group/blob/master/static/images/tpg_ux_5.jpg)

User Selects Companies #1:
![alt tag](https://github.com/Astayonix/perihelion_group/blob/master/static/images/tpg_ux_6.jpg)

User Selects Companies #2:
![alt tag](https://github.com/Astayonix/perihelion_group/blob/master/static/images/tpg_ux_7.jpg)

User's TPG Portfolio Visualization #1:
![alt tag](https://github.com/Astayonix/perihelion_group/blob/master/static/images/tpg_ux_8.jpg)

User's TPG Portfolio Visualization #2:
![alt tag](https://github.com/Astayonix/perihelion_group/blob/master/static/images/tpg_ux_9.jpg)

User's Portfolio Detail Modal Window:
![alt tag](https://github.com/Astayonix/perihelion_group/blob/master/static/images/tpg_ux_10.jpg)

<h5> Technical Stack </h5>
Python, Javascript, Flask, Jinja, jQuery, SQLAlchemy, D3.js, HTML/CSS, Bootstrap, Import.io, JSON, SQLAlchemy, SQLite, and RegEx for Python

<h5> Feature List </h5>
- SQLite Database
  - Used Import.io to scrape all of Nasdaq.com for db contents 
  - Seeded db with all available dividend information from Nasdaq.com
  - Tables for Users, Sectors, Industries, Stocks, Stock Quote Summaries, Dividend Summaries, and Stock Users
- User Accounts
  - Users can sign up and login.
  - Users can create stock portfolio profiles based on whether or not they wish to speculate (whether or not they want *only* stocks yielding dividends)
    - If users chose not to speculate, only stocks yielding a dividend will be returned from the db for investment consideration.
    - If users chose to speculate, all stocks will be returned from the db for investment consideration.
  - Users can visualize their stock portfolio profiles through a nested heat-map of company dividends relative to all other companies in their investment portfolio.
  - Users can open a modal window that displays more information about the companies they've chosen to include in their portfolios.

- D3js
  - Wrote a circle-nesting algorithm that embeds companies within their respective industries and industries within their respective sectors within the overall economy.
  - Created a green-to-white heat map that gives users a quick visual representation of how large individual company's dividend yields are in relation to all other companies in the user's portfolio.

- Boostrap.js/HTML/CSS
  - Integrated front-end styling with Bootstrap.js

<h5> Favorite Challenges </h5>
- Tackling the D3.js nested circle pack layout
- Discovering the Jinja for-loop on Nasdaq.com's Dividend Summary page
- Seeding the database using RegEx in Python
- Researching the machine learning for the country predictive model (v 2.0) 
- Scraping Nasdaq.com with Import.io
- Thinking of various ways to visualize the data in an "out-of-the-box" way

<h5> A Special Thanks To </h5>
- The Entire Hackbright Academy Staff
- Katie Lefevre
- Rachel Thomas
- Meggie Mahnken
- Kristen McClure
- Denise Wiedl
- Deborah Erba
- Rahul Choudhury
- Katrina Hall-Hutzley
- Mike Ryan
- DJ Breslin
- Cynthia Burns
- Chris Burns
- Jessie Burns