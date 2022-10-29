from flask import Flask, url_for, render_template, request, redirect, session, Blueprint
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
app.app_context().push()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    def __init__(self, email, password):
        self.email = email
        self.password = password




@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('main.html')
    else:
        return render_template('index.html', message="Welcome!")



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(email=request.form['email_in'], password=request.form['password_in']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('register.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['email_in']
        p = request.form['password_in']
        data = User.query.filter_by(email=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('main'))
        return render_template('login.html', message="Incorrect Details")

@app.route('/main', methods=['GET'])
def main():
    if session.get('logged_in'):
        return render_template('main.html', message="Welcome!")
    else:
        return render_template('index.html', message="Welcome!")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))




if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p4234324343"
    db.create_all()
    app.run(debug=True)