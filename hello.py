from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment 
from datetime import datetime 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, NoneOf, ValidationError
from flask import Flask, render_template, session, redirect, url_for, flash
from email_validator import validate_email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

#source for validate function: http://wtforms.simplecodes.com/docs/0.6/validators.html
def validate_email(form, field):
     if "@" not in field.data:
         raise ValidationError('Please include an @ in the email address. '+field.data+' is missing an @.')

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address?', validators=[DataRequired(), validate_email])
    submit = SubmitField('Submit')
 
@app.route('/', methods=['GET', 'POST'])
def index():
	email = ""
	name = ""
	form = NameForm()
			#return render_template('index.html', form=form, name = name)
	#form = NameForm()
	if form.validate_on_submit():
		old_name = session.get('name') 
		old_email = session.get('email')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		if old_email is not None and old_email != form.email.data:
			flash('Looks like you have changed your email!')
		session['name'] = form.name.data 
		session['email'] = form.email.data
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name = session.get('name'), 	email=session.get('email'))
	

	