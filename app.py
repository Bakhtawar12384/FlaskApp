from flask import Flask, render_template, request  # ✅ added request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///firstapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define model
class FirstApp(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.fname}"

# Modified route to handle GET and POST
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # Get data from the HTML form
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']

        # Create new record object
        entry = FirstApp(fname=fname, lname=lname, email=email)
        db.session.add(entry)
        db.session.commit()

    # Fetch all records from the table to display
    allpeople = FirstApp.query.all()

    # Pass data to template
    return render_template('index.html', allpeople=allpeople)

@app.route('/home')
def home():
    return 'Welcome to the Home Page'

if __name__ == '__main__':
    # ✅ Create tables before running (only needed once)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
