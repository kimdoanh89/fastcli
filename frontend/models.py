from frontend import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    config_file = db.Column(db.Text, nullable=False)
    inventory_file = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    devices = db.relationship('Device', backref='project', lazy=True)

    def __repr__(self):
        return f"Project('{self.name}', '{self.date_created}', '{self.config_file}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    projects = db.relationship('Project', backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    version = db.Column(db.String(100), nullable=False, default='-')
    platform = db.Column(db.String(100), nullable=False, default='-')
    image_id = db.Column(db.String(100), nullable=False, default='-')
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    management_ip = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Device('{self.name}', Project ID: '{self.project_id}', Managemet IP: '{self.management_ip}')"
    
    def add_device(name, project_id, management_ip):
        device = Device(name=name, project_id=project_id, management_ip=management_ip)
        db.session.add(device)
        db.commit()
