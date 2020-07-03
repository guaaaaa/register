from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///register.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Register' + str(self.id)

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        register_name = request.form['name']
        register_email = request.form['email']
        register_subject = request.form['subject']
        register_content = request.form['content']
        new_user = UserRegister(name=register_name, email=register_email, subject=register_subject, content=register_content)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/register/success')
    else:
        return render_template('register.html')

@app.route('/register/success', methods=['GET'])
def success():
    if request.method == 'POST':
        register_name = request.form['name']
        register_email = request.form['email']
        register_subject = request.form['subject']
        register_content = request.form['content']
        new_user = UserRegister(name=register_name, email=register_email, subject=register_subject, content=register_content)
        db.session.add(new_user)
        db.session.commit()
    else:
        
        new_user = db.session.query(UserRegister).order_by(UserRegister.id.desc()).limit(1)
        return render_template('success.html', user=new_user)


if __name__ == "__main__":
    app.run(debug=True)