# """ Distributes the initial investment amongst the companies in the user's portfolio"""

initial_investment = int(50000)
companies={"Acer":{35:0.04},"Coke":{20:0.1},"Disney":{15:0.75},"Boeing":{7:0.9},"Hackbright":{100:1}}
lasttradelist=[]
dividendlist=[]
# our_list = []
# for key in companies: 
#     our_list.append((companies[key][0:3], companies[key][3:]))

for companynames in companies:
    companynames = companies.keys()
print companynames
numofcompanies = len(companies.keys())
print numofcompanies

for valuesdict in companies:
    valuesdict = companies.keys()
    lasttradelist[valuesdict].iterkeys()
print lasttrade
print valuesdict
print initial_investment

# so let's say you have a dictionary with information about companies and their
# yearly dividends that looks like this:
# (please excuse my lack of knowledge about what a dividend looks like)
dividends = {'company1':
             {'2015': '5',
              '2014': '4',
              '2013': '5'},
             'company2':
             {'2015': '10',
              '2014': '13',
              '2013': '9'}
             }

# let's say we wanted to return all years we have dividends for:
years = {}
for company in dividends.iterkeys():
    years[company] = dividend[company].keys()

# this make our years variable look something like this:
{'company2': ['2015', '2014', '2013'], 'company1': ['2015', '2014', '2013']}

# maybe we know all of the companies have the same dividend years in our
# dividends dictionary, and we just want a list for each of the actual return
# value
returns = {}
for company in dividends.iterkeys():
    # make a variable to store off the returns as we iterate
    company_returns = []
    # iterate over the second-level keys in our nested dictionary
    for year in dividend[company].iterkeys():
        # and add each year to our compnay_returns list
        company_returns.append(dividend[company][year])
    # then add the list of this company's returns to our returns dictionary
    # with the company as the key
    returns[company] = company_returns

# in this case, returns will look like this:
{'company2': ['10', '13', '9'], 'company1': ['5', '4', '5']}

# we have some problems, though; because we're working with dictionaries,
# we can't confirm the order that we get our dividend values back in
# so we maybe want to sort the years before we use them to get our values:
sorted_dividends = {}
for company in dividends.iterkeys():
    # let's sort the years -- default behavior is ascending
    years[company].sort()
    # make a variable to store off the list of returns we're making
    sorted_dividends[company] = []
    # iterate over the years for this company
    for year in years[company]:
        # add the dividend to this company's values in
        # sorted_dividends[company]
        dividend = dividend[company][year]
        sorted_dividends[company].append(dividend)

# this will make sorted_dividends look like this:
{'company2': ['9', '13', '10'], 'company1': ['5', '4', '5']}
# and because we sorted the list of years and we know they cover the same
# years, we know they're in the right order

# since we know the years covered in our data, or maybe we know what years we
# want to cover, OR we know there are some companies with years we don't want
# we could also do something like this:

# make a variable to store off our data
dividends_by_specific_years = {}
# make a list of the years we want dividends for in the order we want them
# output
dividend_years = ['2013', '2014']
# iterate over all of the companies we have data for
for company in dividends.iterkeys():
    dividends_by_specific_years[company] = []
    # get the values for the years we specified
    for year in dividend_years:
        dividend = dividends[company][year]
        # store off the value in the variable we started with
        dividends_by_specific_years[company].append(dividend)

# this will make dividends_by_specific_years look like this:
{'company2': ['9', '13'], 'company1': ['5', '4']}