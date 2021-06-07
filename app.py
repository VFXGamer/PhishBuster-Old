from flask import Flask, request, render_template, redirect, jsonify
import phishbuster as pb

app = Flask(__name__,template_folder='static')

@app.route("/")
def index():
    selecturl = [["github.com","Github"],
    ["twitter.com","Twitter"],["google.com",'Google'],
    ["amazon.com",'Amazon'],["netflix.com",'Netflix'],
    ["wikipedia.org",'Wikipedia'],["reddit.com",'Reddit'],
    ["zoom.us",'Zoom'],["walmart.com",'Walmart'],["instagram.com",'Instagram'],
    ["wordpress.com",'Wordpress'],["paypal.com",'Paypal']]# List of Names and urls to show in the drop down menu
    selecturl.sort()
    selecturl = [["select","Select"]]+selecturl
    return render_template("index.html",selecturl=selecturl)

@app.route('/check', methods=["GET","POST"])
def check():
    if request.method == "POST":
        req = request.form
        inurl = req['inurl'] # Storing input url in a variable
        seurl = req['seurl'] # Storing url from drop down menu in a variable
        if inurl != '' and seurl != 'select':
            output = pb.comparing_url(inurl,seurl)
            if output == True:
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
