from flask import Flask, render_template,redirect,url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import generate_csrf



app = Flask(__name__)
csrf = CSRFProtect(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'userside'
app.secret_key = 'random-secret-key'

mysql = MySQL(app)

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("EMail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("EMail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class RailwayRegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    employeeid = StringField("EmployeeID", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class RailwayLoginForm(FlaskForm):
    employeeid = StringField("EmployeeID", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


@app.route('/')
def index():
    return "flask-auth-sys"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM userdata WHERE email = %s",(email,))
        mysql.connection.commit()
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            flash("Login Failed")
            return redirect(url_for('login'))
    return render_template('userindex.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    csrf_token = generate_csrf()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO userdata (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template('usersign.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("logged out successfully")
    return redirect(url_for('login'))

@app.route('/railwaysignup', methods = ['GET', 'POST'])
def railwaysignup():
    form = RailwayRegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        employeeid = form.employeeid.data      
        password1 = form.password.data       
        hashed_password1 = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO railwaydata (name, email, employeeid, password1) VALUES (%s, %s, %s, %s)",(name, email, employeeid, hashed_password1))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('railwaylogin'))
    return render_template('railwaysignup.html', form=form)

@app.route('/railwaylogin', methods=['GET', 'POST'])
def railwaylogin():
    form = RailwayLoginForm()
    if form.validate_on_submit():
        employeeid = form.employeeid.data
        password1 = form.password.data
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM railwaydata WHERE employeeid = %s", (employeeid,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password1.encode('utf-8'), user[4].encode('utf-8')):
            session['user_id'] = user[0]
            print("User ID:", session['user_id']) 
            return redirect(url_for('dashboard')) 
        else:
            flash("Login Failed")
            return redirect(url_for('railwaylogin')) 
    return render_template('railwaylogin.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
    