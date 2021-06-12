from flask import Flask, request, render_template, redirect, jsonify
import phishbuster as pb
from flaskext.mysql import MySQL

app = Flask(__name__,template_folder='static')
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'dbname'
app.config['MYSQL_DATABASE_HOST'] = 'servername'
mysql.init_app(app)
connect = mysql.connect()

@app.route("/")
def index():
    cursor = connect.cursor()
    #execute select statement to fetch data to be displayed in dropdown
    cursor.execute('SELECT names,domains FROM domain_data')
    db_output = cursor.fetchall()
    lis = list(db_output)
    lis.sort()
    selecturl = [["Select","select"]]+lis
    return render_template("index.html",selecturl=selecturl)

@app.route('/check', methods=["GET","POST"])
def check():
    if request.method == "POST":
        req = request.form
        inurl = req['inurl'] # Storing input url in a variable
        seurl = req['seurl'] # Storing url from drop down menu in a variable
        if inurl != '' and seurl != 'select':
            output = pb.comparing_url(inurl,seurl)
            if output is True:
                with open('static/reports.txt', 'a+') as p:
                    p.write('\n'+seurl+'\t'+inurl) # Stores all the phishing urls in reports.txt
                return redirect('/phishing') # Redirects to It is  PHISHING SITE
            else:
                return redirect('/safe') # Redirects to It is SAFE SITE
        else:
            return redirect('/') # Redirects to home page if vlaues are not entered
    return redirect('/')

@app.route("/phishing")
def phish():
    return render_template("phish.html")

@app.route("/safe")
def safe():
    return render_template("safe.html")

@app.route("/api/<string:urlin>+<string:urlse>")
def api(urlin,urlse):
    output = pb.comparing_url(urlin,urlse)
    return jsonify({
        'Input Url':urlin,
        'Orginal Url':urlse,
        'Phishing Site':output
        })

if __name__ == '__main__':
    app.run(debug=True)
