from flask import Flask, request, render_template, redirect, jsonify, flash, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import phishbuster as pb
from flaskext.mysql import MySQL
import requests
import os

app = Flask(__name__,template_folder='static')
limiter = Limiter(app, key_func=get_remote_address) # Limiter setup for PhishBuster API
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = os.environ['user']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['password']
app.config['MYSQL_DATABASE_DB'] = os.environ['dbname']
app.config['MYSQL_DATABASE_HOST'] = os.environ['servername']

mysql.init_app(app) 

header = ['Sr No.', 'Orginal Site', 'Phishing Site','Action'] # Header for reports table

def mysqldata_insert(seurl,inurl): # For appending values to reports_data table
    try:
        connect = mysql.connect() # for connecting to the database
        cursor = connect.cursor() # cursor to execute mysql queries
        cursor.execute(f"INSERT INTO reports_data(org_site,phish_site) VALUES ('{seurl}','{inurl}')") # mysql query to append data to the dataabase
        connect.commit() # commit changes to database
        print('Commited Successfully')
    except Exception as e:
        print(e)
        connect.rollback() # undo changes if error occured while appending data to the database

# index page
@app.route("/")
def index():
    try:
        connect = mysql.connect() # for connecting to the database
        cursor = connect.cursor() # cursor to execute mysql queries
        cursor.execute('SELECT names,domains FROM domain_data') # mysql query to get all the data from the database
        db_output = cursor.fetchall() # fetching all the data from the database
        lis = list(db_output) # converting tuple to list
        lis.sort() # sorting the list
        selecturl = [["Select Site","select"]]+lis # appending the list to the list
        cursor.execute('SELECT country_name,country_code FROM countries') # mysql query to get all the data from the database
        db_output2 = cursor.fetchall() # fetching all the data from the database
        lis2 = list(db_output2) # converting tuple to list
        lis2.sort() # sorting the list
        countrydata = [["Select Country","select"]]+lis2 # appending the list to the list
        return render_template("index.html",selecturl=selecturl,countrydata=countrydata) # selecturl sends list containing list of real sites
    except Exception as e:
        print(e)
        selecturl = [["Error Occured to connect with DB","select"]] # if error occured while fetching data from the database
        countrydata = [["Error Occured to connect with DB","select"]] # if error occured while fetching data from the database
        return render_template("index.html",selecturl=selecturl,countrydata=countrydata) # selecturl sends error as it failed to get data from the database
    return redirect('/')

# For getting values from index and passing them to PhishBuster
@app.route('/check', methods=["POST"])
def check():
    if request.method == "POST":
        req = request.form 
        inurl = req['inurl'] # Storing input url in a variable
        seurl = req['seurl'] # Storing url from drop down menu in a variable
        country = req['country'] # Storing country's iso code in a variable
        inurl = inurl.lower() # Converting input url to lower case to avoid errors
        if inurl != '' and seurl != 'select' and country != 'select':
            output = pb.comparing_url(inurl,seurl,country) # Returns 'True' if it is a phishing site or 'False' if it is a safe site
            if output is True:
                mysqldata_insert(seurl,inurl) # For appending data if it is a phising site
                return redirect('/phishing') # Redirects to It is  PHISHING SITE
            return redirect('/safe') # Redirects to It is SAFE SITE
        return redirect('/') # Redirects to home page if values are not entered

# reports page
@app.route("/reports")
def reports():
    try:
        connect = mysql.connect() # for connecting to the database
        cursor = connect.cursor() # cursor to execute mysql queries
        cursor.execute('SELECT * FROM reports_data') # '*' here is for id, orginal site and phising site
        db_output = cursor.fetchall()
        # converting to list to pass the data to html
        report = list(db_output)
        return render_template("reports.html",head=header,reports=report) # header for column names and reports for rows/site data
    except Exception as e:
        print(e)
        report = ["Error Occured to connect with DB"] # if error occured while fetching data from the database
        return render_template("reports.html",head=header,reports=report)
    return redirect('/')

# phising label page
@app.route("/phishing")
def phish():
    return render_template("phish.html")

# safe label page
@app.route("/safe")
def safe():
    return render_template("safe.html")

# For deleteing a desired row   
@app.route('/delete/<id>/')
def delete(id):
    connect = mysql.connect() # for connecting to the database
    cursor = connect.cursor() # cursor to execute mysql queries
    cursor.execute(f"DELETE FROM reports_data WHERE id='{id}';") # mysql query to delete data of a row
    connect.commit() # commit changes to the database
    print('Commited Successfully')
    return redirect('/reports') # Redirecting to reports page to show that changes were made successfully

# For manually adding values to the database of reports
@app.route('/manualadd', methods = ['POST'])
def manualadd():
    if request.method == 'POST':
        req = request.form
        seurl = req['org'] # getting values through post request and storing to a variable
        inurl = req['phish'] # getting values through post request and storing to a variable
        mysqldata_insert(seurl,inurl) # To adding data to the database
        return redirect('/reports') # Redirecting to reports page to show that changes were made successfully

@app.route("/api/<string:inurl>+<string:seurl>+<string:country>+<string:save>") # Geeting values from the url
@limiter.limit("50/minute") # Setting a limit of 50 PhishBuster API requests in a minute
def api(inurl,seurl,country,save = 'False'):
    inurl = inurl.lower() # Converting input url to lower case to avoid errors
    seurl = seurl.lower() # Converting url from original domain to lower case to avoid errors
    output = pb.comparing_url(inurl,seurl,country) # Returns 'True' if it is a phishing site or 'False' if it is a safe site
    if save == 'True': # String as the input can be made to anything and to overcoming error if the input is coverted to boolean before filtering
        if output is True:
            mysqldata_insert(seurl,inurl) # To adding data to the database
            return jsonify({'Input Url':inurl,'Orginal Url':seurl,'Phishing Site':output,'Data Saved':bool(save),'Region':country}) # API response with data saved information
        return jsonify({'Input Url':inurl,'Orginal Url':seurl,'Phishing Site':output,'Region':country}) # API response if values are not saved
    return jsonify({'Input Url':inurl,'Orginal Url':seurl,'Phishing Site':output,'Region':country}) # API response if values are not saved

if __name__ == '__main__':
    app.run(debug=True)
