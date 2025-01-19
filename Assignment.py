
### **Flask Practical Assignment**

#### **Part 1: Basics of Flask**
'''
1. **Create a Simple Flask Application**  
   Create a Flask application that displays "Hello, Flask!" when accessed via the root URL (`/`).
'''
from flask import Flask,render_template,request

app=Flask(__name__)
'''@app.route('/')
def welcome():
    return ('Hello, Flask')'''

'''
2. **Dynamic Routes**  
Build a route that accepts a name as a URL parameter and displays a personalized greeting.
For example, accessing `/greet/Manav` should display: "Hello, Manav!"'''

@app.route('/greet/<guest>')
def greet(guest):
    return f'Hello {guest}'

'''
3. **HTML Templates**
Use a Flask render_template function to serve an HTML page. 
The HTML page should display a message like "Welcome to Flask Templates!".'''

@app.route('/welcometemplate')
def welcome_template():
    return render_template ('welcome.html')


#### **Part 2: Forms and User Input**
'''
4. **Handle GET and POST Methods**  
   Create a route `/form` that displays an HTML form with fields for a user's name and age. 
   Handle the form submission using POST, and display the submitted data on a new page.'''

'''
5. **Form Validation**  
Modify the form from question 4 to ensure that both fields (name and age) are required.
If the form is submitted empty, display an error message.'''
@app.route('/form',methods=['GET','POST'])
def form():
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        if not name or not age:
            return ('error: name and age both required')
        return (f'Name:{name},age:{age}')
        
    return render_template('form.html')
'''
#### **Part 3: Flask Extensions**
6. **Flask-WTF**  
   Use Flask-WTF to create a form with fields for an email address and password. 
   Validate the email format and ensure the password is at least 8 characters long.'''

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import Email, Length,DataRequired

app.config['SECRET_KEY']='Prince@123'

class Loginform(FlaskForm):
    email=StringField('email',validators=[DataRequired(),Email()])
    password= PasswordField('password',validators=[DataRequired(),Length(min=8)])

@app.route('/login_1',methods=['GET','POST'])
def login_1():
    form=Loginform()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        return ('Login successful')
    return render_template('login.html',form=form)
'''
7. **Database Integration**  
Use SQLite with Flask to create a database of users.
 Write routes to add a user (via a form) and display all users on another page.'''


#import required libraries
from flask import redirect,url_for
from flask_sqlalchemy import SQLAlchemy

#configure database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='Prince@123'

#Initialize database
db=SQLAlchemy(app)

#create database table model
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(120),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)

#create table
with app.app_context():
     db.create_all()


#add user
@app.route('/add_user',methods=['GET','POST'])
def add_user():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        if name and email:
            new_user=User(name=name,email=email)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('list_users'))
    return render_template('add_user.html')

#print all users
@app.route('/users')
def list_users():
    users=User.query.all()
    return render_template('list_users.html',users=users)

#### **Part 4: Advanced Features**
'''8. **API Creation**  
   Create a Flask route `/api/users` that returns a list of user data in JSON format.'''

users=[{"name":"df","age":54},{"name":"de3","age":84}]
from flask import jsonify
@app.route('/api/users',methods=['GET'])
def api_users():
    return jsonify(users)

'''
9. **Error Handling**  
   Implement a custom 404 error page that displays "Page Not Found" when a non-existent route is accessed.'''
@app.errorhandler(404)
def error_handle(e):
    return render_template('error.html'),404

'''
10. **Session Management**  
Use Flask sessions to store a visitor’s username after login.
On subsequent visits, greet the user by their stored username.'''

from flask import session

app.config['SECRET_KEY']='Prince@123'

@app.route('/')
def home():
    if 'username' in session:
        username=session['username']
        return f"welcome {username} <a href='/logout'>Logout</a>"
    return f"welcome please <a href='/login'>Login</a>"
#login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        session['username']=username
        return redirect(url_for('home'))
    return render_template('css_session.html')

#logout
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))
    
'''
### **Bonus Questions**
- Add Bootstrap or another CSS framework to style your Flask application.
'''

' Deploy your Flask application to a platform like Heroku or PythonAnywhere.'
if __name__=='__main__':
    app.run(debug=True)



