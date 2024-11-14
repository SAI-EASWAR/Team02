from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
db = SQLAlchemy(app)

# Define the Project model
class Project(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    project_owner = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    revised_end_date = db.Column(db.Date, nullable=True)

# Initialize the database
with app.app_context():
    db.create_all()

# Route to render the button page
@app.route('/')
def button():
    return render_template('button.html')

# Route to render the form page
@app.route('/new_project')
def new_project():
    return render_template('form.html')

# Route to handle form submission
@app.route('/create_project', methods=['POST'])
def create_project():
    project_id = request.form['project_id']
    project_name = request.form['project_name']
    project_description = request.form['project_description']
    project_owner = request.form['project_owner']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    revised_end_date = request.form.get('revised_end_date')

    # Parse dates to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    revised_end_date = datetime.strptime(revised_end_date, '%Y-%m-%d').date() if revised_end_date else None

    # Create a new project instance
    new_project = Project(
        project_id=project_id,
        project_name=project_name,
        project_description=project_description,
        project_owner=project_owner,
        start_date=start_date,
        end_date=end_date,
        revised_end_date=revised_end_date
    )

    # Add to the database and commit
    db.session.add(new_project)
    db.session.commit()

    return redirect(url_for('new_project'))  # Redirect back to the form page
    
@app.route('/view_projects')
def view_projects():
    projects = Project.query.all()  # Get all projects from the database
    return render_template('view_projects.html', projects=projects)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)