from flask import Flask, render_template, request, redirect, url_for
from config import Config
from database.db import db
from database.models import Project# Import db and the Project model
from database.queries import add_project, get_all_projects
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the SQLAlchemy app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)
# Initialize Flask-Script Manager to handle command-line tasks



# Create database tables if they don't exist
with app.app_context():
    db.create_all()  # This will create the SQLite tables in projects.db if they don’t exist

@app.route('/')
def button():
    return render_template('button.html')

@app.route('/new_project')
def new_project():
    return render_template('form.html')

@app.route('/create_project', methods=['POST'])
def create_project():
    project_data = {
        'project_id': request.form['project_id'],
        'project_name': request.form['project_name'],
        'project_description': request.form['project_description'],
        'project_owner': request.form['project_owner'],
        'start_date': datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
        'end_date': datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
        'revised_end_date': datetime.strptime(request.form.get('revised_end_date'), '%Y-%m-%d').date() if request.form.get('revised_end_date') else None,
        'status': request.form['status']
    }
    add_project(project_data)
    return redirect(url_for('new_project'))

@app.route('/view_projects')
def view_projects():
    projects = get_all_projects()
    return render_template('view_projects.html', projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
