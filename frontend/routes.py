from frontend import app
from flask import render_template

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

@app.route('/')
@app.route('/home')
def main():
    return render_template('main.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/<id>', methods=['GET'])
def project_info(id):
    """
    This page shows detailed stats on an individual project
    queried by project id
    """
    return render_template('project_detail.html', project=projects[0])