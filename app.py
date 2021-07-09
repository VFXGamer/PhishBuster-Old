from flask import Flask, request, render_template, redirect, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import phishbuster as pb
from flaskext.mysql import MySQL
import os

app = Flask(__name__,template_folder='static')
limiter = Limiter(app, key_func=get_remote_address)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = os.environ['user']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['password']
app.config['MYSQL_DATABASE_DB'] = os.environ['dbname']
app.config['MYSQL_DATABASE_HOST'] = os.environ['servername']

mysql.init_app(app)

header = ['Sr No.', 'Orginal Site', 'Phishing Site']

connect = mysql.connect()
cursor = connect.cursor()

def mysqldata(seurl,inurl):
    try:
        cursor.execute(f"INSERT INTO reports_data(org_site,phish_site) VALUES ('{seurl}','{inurl}')")
        connect.commit()
        print('Commited Successfully')
    except Exception as e:
        print(e)
        connect.rollback()

@app.route("/")
def index():
    try:
        #execute select statement to fetch data to be displayed in dropdown
        cursor.execute('SELECT names,domains FROM domain_data')
        db_output = cursor.fetchall()
        lis = list(db_output)
        lis.sort()
        selecturl = [["Select","select"]]+lis
        return render_template("index.html",selecturl=selecturl)
    except Exception as e:
        print(e)
        selecturl = [["Error Occured to connect with DB","select"]]
        return render_template("index.html",selecturl=selecturl)
    return redirect('/')

@app.route('/check', methods=["POST"])
def check():
    if request.method == "POST":
        req = request.form
        inurl = req['inurl'] # Storing input url in a variable
        seurl = req['seurl'] # Storing url from drop down menu in a variable
        if inurl != '' and seurl != 'select':
            output = pb.comparing_url(inurl,seurl)
            if output is True:
                mysqldata(seurl,inurl)
                return redirect('/phishing') # Redirects to It is  PHISHING SITE
            else:
                return redirect('/safe') # Redirects to It is SAFE SITE
        else:
            return redirect('/') # Redirects to home page if vlaues are not entered
    return redirect('/')

@app.route("/reports")
def reports():
    try:
        connect = mysql.connect()
        cursor = connect.cursor()
        #execute select statement to fetch data to be displayed in dropdown
        cursor.execute('SELECT * FROM reports_data')
        db_output = cursor.fetchall()
        lis = list(db_output)
        return render_template("reports.html",head=header,reports = lis)
    except Exception as e:
        print(e)
        lis = ["Error Occured to connect with DB"]
        return render_template("reports.html",head=header,reports = lis)
    return redirect('/')

@app.route("/phishing")
def phish():
    return render_template("phish.html")

@app.route("/safe")
def safe():
    return render_template("safe.html")

@app.route("/api/<string:inurl>+<string:seurl>+<string:save>")
@limiter.limit("50/minute")
def api(inurl,seurl,save = 'False'):
    inurl.lower()
    seurl.lower()
    output = pb.comparing_url(inurl,seurl)
    if save == 'True':
        if output is True:
            mysqldata(seurl,inurl)
            return jsonify({'Input Url':inurl,'Orginal Url':seurl,'Phishing Site':output,'Data Saved':bool(save)})
        return jsonify({'Input Url':inurl,'Orginal Url':seurl,'Phishing Site':output,}) 
    return jsonify({'Input Url':inurl,'Orginal Url':seurl,'Phishing Site':output})

if __name__ == '__main__':
    app.run()
