from flask import Flask
from flask import render_template
from flask import Flask, request, send_from_directory

app = Flask(__name__)

import db_model as db
import json
import jinja2
import feedbacktemplate
reload(feedbacktemplate)

from datetime import date
from datetime import timedelta
from feedbacktemplate import feedbackTemplate
	
def fillHTMLTemplate(templateString, params):
    """Invokes the jinja2 methods to fill in the slots in the template."""
    templateObject = jinja2.Template(templateString)
    htmlContent = templateObject.render(params)
    return htmlContent
    
def writeHTMLFile(htmlText, filename):
    """Helper file to write the HTML file from the given text. It uses the
       codecs module, which can deal correctly with UTF8 encoding.
    """
    import codecs
    with codecs.open(filename, 'w', 'utf8') as htmlFile:
        htmlFile.write(htmlText)
        
#template: [{u'loc': 'Clapp', u'com': 'this place sucks', u'stars': 2}, {...}, {...}]
#sort by location
#{Clapp: comment}
def parse(l, k):
	comments = []
	for item in l:
		comments.append(item[k])
		print item[k]
	return comments

		
app = Flask(__name__, static_url_path='')

@app.route('/style/<path:path>')
def send_style(path):
    return send_from_directory('style', path)
    
@app.route("/wellesley.html")
def feedback():
	#dict{location:data{name:name, avg:avg, com:[comments, comments, ...]}, location:data{}}
	list= []
	locations = db.select_listlocations()
	print locations
	loclist = [l[u'loc'] for l in locations if u'loc' in l]
	print loclist
	for loc in loclist:
		print loc
		data = {}
		comments = db.select_comments(loc)
		print comments
		comlist = [c[u'com'] for c in comments if u'com' in c]
		average = db.select_average(loc)
		print average
		data['name'] = loc
		data['avg'] = "%.2f" % round(average[0][u'AVG'],2)
		data['com'] = comlist
		print data
		list.append(data)
	print "***" 
	print list
	parsresults = {'dict':list}
	htmlText = fillHTMLTemplate(feedbackTemplate, parsresults)
	writeHTMLFile(htmlText, "templates/feedback.html")
	return render_template("feedback.html")

@app.route("/review.html")
def review():
    return render_template("review.html")
  
@app.route("/review.html", methods=['POST'])
def review_post():
	if request.method == 'POST':
		l = request.form['location']
		print l
		c = request.form['comment']
		s = request.form['stars']
		db.write_data(l, c, s)
		feedback()
		print "done"
	return render_template("shortcut.html")
	    
@app.route("/thanks.html", methods = ["POST"])
def thanks():
    return render_template("thanks.html")

@app.route("/index.html")
def index():
    results = db.select_one()
    return render_template("index.html")
    
@app.route("/")
def shortcut():

    results = db.select_one()

    return render_template("shortcut.html")
    
TEMPLATES_AUTO_RELOAD = True

if __name__ == "__main__":
    app.run('0.0.0.0')
    app.run(debug=True)
    



