from frontend import app, db, bcrypt
from flask import render_template, flash, redirect, url_for
from frontend.forms import RegistrationForm, LoginForm, ProjectForm
from frontend.models import User, Project, Device
from flask_login import login_user, current_user, logout_user
import yaml


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('project'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('project'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('project'))
        else:
            flash('Login Unsuccessfully. Please check Username and Password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/project')
def project():
    return render_template('project.html', projects=current_user.projects)


@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        new_project = Project(name=form.name.data, description=form.description.data,
                              config_file=form.configFile.data, user_id=current_user.id,
                              inventory_file=form.inventoryFile.data)
        db.session.add(new_project)
        db.session.commit()
        # flash('New project has been created!', 'success')
        with open(form.inventoryFile.data, 'r') as f:
            device_list = yaml.full_load(f)
        for hostname, values in device_list.items():
            device = Device(name=hostname, project_id=new_project.id, management_ip=values['hostname'])
            db.session.add(device)
            db.session.commit()
        return redirect(url_for('project'))
    return render_template('add_project.html', title='Add Project', form=form)


@app.route('/project/<project_id>', methods=['GET'])
def project_info(project_id):
    """
    This page shows detailed stats on an individual project
    queried by project id
    """
    return render_template('project_detail.html', project=Project.query.filter_by(id=project_id).first())


@app.route('/project/<project_id>/configure', methods=['GET', 'POST'])
def configure(project_id):
    return render_template('configure_project.html', title='Configure Project',
                           project=Project.query.filter_by(id=project_id).first())

from nornir import InitNornir
from constants import config_file
from nafc.api.show import get_config
nr = InitNornir(config_file=f"{config_file}")
result = nr.run(task=get_config, command="sh config")
@app.route('/project/<project_id>/configure/<device>', methods=['GET', 'POST'])
def current_configure(project_id, device):
    # result = run_get_config("sh config", False, False, "R1")
    x = result[device][1].result
    with open(f'{device}.txt', 'w') as a:
       a.write(x)
    # x = print(x)
    return render_template('configure_project.html', title='Configure Project',
                           project=Project.query.filter_by(id=project_id).first(),
                           device=Device.query.filter_by(project_id=project_id, name=device).first(),
                           result=x)
