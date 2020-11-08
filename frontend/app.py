from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fastcli.sqlite3'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

projects = [
    {
        'id' : 1,
        'name': 'BGP',
        'author': 'Doanh',
        'date': '20-Jul-2020',
        'config_file': 'inventory/bgp/config.yaml'
    },
    {
        'id' : 2,
        'name': 'OSPF',
        'author': 'Dan',
        'date': '21-Jul-2020',
        'config_file': 'inventory/ospf-eigrp-rip/config.yaml'
    }
]

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))


@app.route('/')
@app.route('/home')
def main():
    return render_template('main.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/<id>', methods=['GET'])
# def project_info(id):


if __name__ == '__main__':
    Bootstrap(app)
    app.run(debug=True)