from flask import Flask, render_template
from passlib.hash import pbkdf2_sha256

from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# Configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://kcszumbnyngcpe:b6bff3fa03331de5fa50e583ab82b05524c0e1b1551fdc98673a56c558fbff29@ec2-35-168-54-239.compute-1.amazonaws.com:5432/d8ru7iuptl4q1i'
db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():

	reg_form = RegistrationForm()
	if reg_form.validate_on_submit():
		username = reg_form.username.data
		password = reg_form.password.data

		# Hashing the password
		hashed_pswd = pbkdf2_sha256.hash(password)

		# If no such username add the user to the database
		user = User(username=username, password=hashed_pswd)
		db.session.add(user)
		db.session.commit()
		return "Inserted into the database"

	return render_template("index.html", form=reg_form)

if __name__ == "__main__":
	app.run(debug=True)