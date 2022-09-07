from flask import Flask, render_template, flash, request, redirect, url_for

from datetime import datetime


#Create a Flask Instance
app = Flask(__name__)

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/topic')
def topic():
	return render_template("topic.html")	

# Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error 
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500	