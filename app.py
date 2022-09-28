from flask import Flask, render_template, flash, request, redirect, url_for

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField, BooleanField, ValidationError, TextAreaField 
from wtforms.validators import DataRequired, EqualTo, Length 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_ckeditor import CKEditor

from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename
import uuid as uuid
import os
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#from flaskext.mysql import MySQL

app = Flask(__name__)
#app.run(use_reloader=True)
#app.config["DEBUG"] = True
#mysql = MySQL()
#app.config['MYSQL_DATABASE_USER'] = 'marco873'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'Mandorladespina1'
#app.config['MYSQL_DATABASE_DB'] = 'marco873$viewers'
#app.config['MYSQL_DATABASE_HOST'] = 'marco873.mysql.pythonanywhere-services.com'
#mysql.init_app(app)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


ckeditor = CKEditor(app)

# Flask login stuffflask
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_viewr(viewr_id):
	return Viewrs.query.get(int(viewr_id))


#DATABASE SECTION Starts_______________________________________________________
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# DATA SECTION
# after create_db.py
# In terminal
# $ python create_db.py

# HOW TO INITIATE MYSQL DATABASE FROM TERMINAL
# flask db init

# HOW TO DO FIRST MIGRATION FROM TERMINAL
# $ flask db migrate -m 'Initial Migration'
# $ flask db upgrade

# THE SAME TO DO FOLLOWING MIGRATION FROM TERMINAL
# $ flask db migrate -m 'DESCRIPTIVE NOTES'
# $ flask db upgrade
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

#  SQL Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///viewer.db'
#  MYSQL Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mandorladespina1@localhost/viewers'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://marco873:Mandorladespina1@marco873.mysql.pythonanywhere-services.com/marco873$viewers'
# Secret Key
app.config['SECRET_KEY'] = "hard to guess"
#Initialize DataBase
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db = SQLAlchemy(app)
migrate = Migrate(app, db)

#DATABASE SECTION Ends_________________________________________________________

#@app.route('/') SECTION Starts________________________________________________

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Viewrs.query.filter_by(username= form.username.data).first()
		if user:
			if check_password_hash(user.password_hash, form.password.data ):
				login_user(user)
				flash("Login Successfully!")
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Password _ Try Again!")
		else:
			flash("That User Doesn't Exist _ Try Again...")
	return render_template('login.html', form=form)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged out! Thanks For Visiting...")
	return redirect(url_for('login'))
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/search', methods=['POST'])
def search():
	form = SearchForm()
	posts = Posts.query

	if form.validate_on_submit():
		post.searched = form.searched.data
		posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
		posts = posts.order_by(Posts.title).all()
		return render_template("search.html", form=form, searched = post.searched, posts=posts)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/dashboard', methods=['GET', 'POST'])
@ login_required
def dashboard():
	form = VieweForm()
	id = current_user.id
	name_to_update = Viewrs.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.profession = request.form['profession']
		name_to_update.username = request.form['username']
		name_to_update.about_author = request.form['about_author']
		

		if request.files['profile_pic']:
			name_to_update.profile_pic = request.files['profile_pic']
			pic_filename = secure_filename(name_to_update.profile_pic.filename)
			pic_name = str(uuid.uuid1()) + "_" + pic_filename
			saver = request.files['profile_pic']
			name_to_update.profile_pic = pic_name

			try:
				db.session.commit()
				saver.save(os.path.join(app.config['UPLOAD_FOLDER'],pic_name))
				flash(" Updated Successfully!")
				return render_template("dashboard.html",
					form=form,
					name_to_update = name_to_update)
			except:
				flash("Error...try again!")
				return render_template("dashboard.html",
					form=form,
					name_to_update = name_to_update)
		else:
			db.session.commit()
			flash(" Updated Successfully!")
			return render_template("dashboard.html", form=form, name_to_update = name_to_update)
	else:
		db.session.commit()
		#flash("Updated Successfull!")
		return render_template("dashboard.html", form=form, name_to_update = name_to_update, id=id)



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/delete/<int:id>')
@login_required
def delete(id):
	viewer_to_delete = Viewrs.query.get_or_404(id)
	name = None
	form = VieweForm()
	try:
		db.session.delete(viewer_to_delete)
		db.session.commit()
		flash("Viewer Deleted Successfully!")

		our_viewers = Viewrs.query.order_by(Viewrs.date_added)
		return render_template("add_viewer.html",
		name = name,
		form = form,
		our_viewers=our_viewers)

	except:
		flash("Whoops! There was a problem deleting user. Try again!")
		our_viewers = Viewrs.query.order_by(Viewrs.date_added)
	return render_template("add_viewer.html",
		name = name,
		form = form,
		our_viewers=our_viewers)

#else:
	#flash("Sorry, you can't delete that user!")
	#return redirect(url_for('dashboard'))
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/')
def index():
	return render_template("index.html")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/about')
def about():
	return render_template("about.html")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/impressum')
def impressum():
	return render_template("impressum.html")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/products')
def products():
	return render_template("products.html")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#STEP-3:
@app.route('/viewer/add', methods=['GET','POST'])
def add_viewer():
	name = None
	form = VieweForm()
	if form.validate_on_submit():
		viewer = Viewrs.query.filter_by(email=form.email.data).first()
		if viewer is None:
			hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
			viewer = Viewrs(username=form.username.data, name=form.name.data, email=form.email.data, profession=form.profession.data, password_hash=hashed_pw)
			db.session.add(viewer)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.username.date = ''
		form.email.data = ''
		form.profession.data = ''
		form.password_hash.data = ''
		flash("Viewer Added Successfully!")
	
	our_viewers = Viewrs.query.order_by(Viewrs.date_added)
	return render_template("add_viewer.html",
		name = name,
		form = form,
		our_viewers=our_viewers)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#STEP:4
@app.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
	form = VieweForm()
	name_to_update = Viewrs.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.profession = request.form['profession']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("Viewer Updated SuccessfullY!")
			return render_template("dashboard.html",
				form=form,
				name_to_update = name_to_update,
				id=id)

		except:
			flash("Error! Try again!")
			return render_template("update.html",
				form=form,
				name_to_update = name_to_update,)
	else:
		return render_template("update.html",
				form=form,
				name_to_update = name_to_update,
				id=id )
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++		
@app.route('/add-post', methods=['GET', 'POST'])
@ login_required
def add_post():
	form = PostForm()
	if form.validate_on_submit():
		poster = current_user.id
		post = Posts(title=form.title.data, content=form.content.data, slug=form.slug.data, poster_id=poster)
		# CLEAR THE FORM
		form.title.data = ''
		form.content.data = ''
		#form.author.data = ''
		form.slug.data = ''
		# ADD POST DATA TO DATABASE
		db.session.add(post)
		db.session.commit()

		flash("Blog Post Submitted Successfully!")
	# REDIRECT TO WEBPAGE
	return render_template("add_post.html", form=form)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/posts')
#@ login_required
def posts():
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template("posts.html", posts=posts)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.route('/posts/<int:id>')
#@ login_required
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@ login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		#post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data

		db.session.add(post)
		db.session.commit()
		flash("Post Has Been updated!")
		return redirect(url_for("post", id=post.id))

	if current_user.id == post.poster_id or current_user.id == 33:

		form.title.data = post.title
		#form.author.data = post.author
		form.slug.data = post.slug
		form.content.data = post.content
		return render_template('edit_post.html', form=form)
	else:
		flash("You Aren't Authorized To Edit This Post!")
		post = Posts.query.get_or_404(id)
		return render_template('post.html', post=post)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)
	id = current_user.id
	if id == post_to_delete.poster.id or current_user.id == 33:

		try:
			db.session.delete(post_to_delete)
			db.session.commit()
			flash("Blog Post Deleted Successfully!")
			posts = Posts.query.order_by(Posts.date_posted)
			return render_template("posts.html", posts=posts)
		except:
			flash("WHOOPS there was a problem deleting post, Try Again...")
			posts = Posts.query.order_by(Posts.date_posted)
			return render_template("posts.html", posts=posts)
	else:
			flash("You are not Authorized to delete that post!")
			posts = Posts.query.order_by(Posts.date_posted)
			return render_template("posts.html", posts=posts)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#@app.route('/') SECTION Ends________________________________________________


#USING BOOTSTRAPP FORMS IN HTML________________________________________________
#AND creating a python list

topics = []

@app.route('/topic')
def topic():
	flash("Submit a new Topic")
	return render_template("topic.html")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++		
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():	
		name = request.form.get("name")
		topic = request.form.get("topic")
		email = request.form.get("email")
		topics.append(f"{name}|| {topic} || { email}")
		return render_template("admin.html", topics=topics)
	
	
# IT WILL WORK TILL SERVER IS UP AFTER ALL THE DATA WILL BE LOST 
#_____________________________________________________________________________	

# Create Custom Error Pages Stars___________________________________________________
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Internal Server Error 
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500	

# Create Custom Error Pages Ends___________________________________________________

# STEP-2:CREATE FORM CLASS TO CONTAIN DATABASE Starts_________________________________________________________
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++	
class VieweForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	profession = StringField("Profession")
	about_author = TextAreaField("About Author")
	password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
	password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
	profile_pic = FileField("Profile Pic")
	submit = SubmitField("Submit")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PostForm(FlaskForm):
	title = StringField("Selected-Topic", validators=[DataRequired()])
	#content = StringField("Content", validators=[DataRequired()], widget=TextArea())
	content = CKEditorField('Content', validators=[DataRequired()])
	#author = StringField("Author")
	slug = StringField("Slug", validators=[DataRequired()])
	submit = SubmitField("Submit")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# CREATE FORM CLASS Ends_________________________________________________________

# STEP-1:CREATE MODEL FOR DATABASE Starts_________________________________________________________
# model 1:
class Viewrs(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	email =	db.Column(db.String(120), nullable=False, unique=True)
	profession = db.Column(db.String(120))
	about_author = db.Column(db.Text(500), nullable=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	profile_pic = db.Column(db.String(1000))
	password_hash = db.Column(db.String(128))

	posts = db.relationship('Posts', backref='poster')
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute!')
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
	# Create a String
	def __repr__(self):
		return '<Name %r>' % self.name
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# model 2:
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	#author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))
	poster_id = db.Column(db.Integer, db.ForeignKey('viewrs.id'))
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	

# CREATE MODEL Ends_________________________________________________________

# pip install list  starts__________________________________________________

# pip install flask
# pip install flask-wtf
# pip install flask-sqlalchemy
# pip install Flask-Migrate
# pip install mysql-connector
# pip install mysql-connector-python
# pip install mysql-connector-python-rf
# pip install pymysql
# pip install crypthography
# pip install flask_login
# pip install flask-ckeditor




# pip install list  ends____________________________________________________

