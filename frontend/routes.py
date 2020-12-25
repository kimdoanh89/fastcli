from frontend import app, db, bcrypt
from flask import render_template, flash, redirect, url_for
from frontend.forms import RegistrationForm, LoginForm, ProjectForm, MonitorForm
from frontend.models import User, Project, Device
from flask_login import login_user, current_user, logout_user
import yaml
import json

from nornir import InitNornir
from constants import config_file
from nafc.api.show import get_config

nr = InitNornir(config_file=f"{config_file}")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("project"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to login!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("project"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("project"))
        else:
            flash("Login Unsuccessfully. Please check Username and Password!", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/project")
def project():
    return render_template("project.html", projects=current_user.projects)


@app.route("/add_project", methods=["GET", "POST"])
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        new_project = Project(
            name=form.name.data,
            description=form.description.data,
            config_file=form.configFile.data,
            user_id=current_user.id,
            inventory_file=form.inventoryFile.data,
        )
        db.session.add(new_project)
        db.session.commit()
        # flash('New project has been created!', 'success')
        with open(form.inventoryFile.data, "r") as f:
            device_list = yaml.full_load(f)
        for hostname, values in device_list.items():
            device = Device(
                name=hostname,
                project_id=new_project.id,
                management_ip=values["hostname"],
            )
            db.session.add(device)
            db.session.commit()
        return redirect(url_for("project"))
    return render_template("add_project.html", title="Add Project", form=form)


@app.route("/project/<project_id>", methods=["GET"])
def project_info(project_id):
    """
    This page shows detailed stats on an individual project
    queried by project id
    """
    multi_result = {}
    result2 = nr.run(task=get_config, command="sh version")
    for device, device_result in result2.items():
        structured_device_result = device_result[
            1
        ].scrapli_response.genie_parse_output()
        multi_result[device] = structured_device_result
        # print(multi_result)

    return render_template(
        "project_detail.html",
        project=Project.query.filter_by(id=project_id).first(),
        result=multi_result,
    )


@app.route("/project/<project_id>/monitor", methods=["GET", "POST"])
def project_monitor(project_id):
    """
    This page shows detailed stats on an individual project
    queried by project id
    """
    form = MonitorForm()
    project = Project.query.filter_by(id=project_id).first()
    form.device.choices = [device.name for device in project.devices]
    form.command.choices = [
        "sh version",
        "sh interfaces",
        "sh clock",
        "sh ntp associations",
        "sh ntp status",
        "sh int description",
        "sh ip int brief",
    ]
    device_name = form.device.data
    command = form.command.data
    multi_result = {}
    if device_name:
        result = None
        nr2 = nr.filter(name=f"{device_name}")
        result = nr2.run(task=get_config, command=command)
        # breakpoint()
        # print(result)
        result_json = result[device_name][1].scrapli_response.genie_parse_output()

        return render_template(
            "monitor_project.html",
            project=project,
            result_raw=result[device_name][1].result,
            result_json=json.dumps(result_json, indent=2),
            form=form,
        )
    else:
        return render_template(
            "monitor_project.html",
            project=project,
            form=form,
        )


@app.route("/project/<project_id>/configure", methods=["GET", "POST"])
def configure(project_id):
    return render_template(
        "configure_project.html",
        title="Configure Project",
        project=Project.query.filter_by(id=project_id).first(),
    )


@app.route("/project/<project_id>/configure/<device>", methods=["GET", "POST"])
def current_configure(project_id, device):
    result = nr.run(task=get_config, command="sh config")
    x = result[device][1].result.splitlines()
    # with open(f'{device}.txt', 'w') as a:
    #    a.write(result[device][1].result)
    x2 = result[device][1].result
    # print(x)
    return render_template(
        "configure_project.html",
        title="Configure Project",
        project=Project.query.filter_by(id=project_id).first(),
        device=Device.query.filter_by(project_id=project_id, name=device).first(),
        result=x,
        result2=x2,
    )
