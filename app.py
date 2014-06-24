#-------------------------------------------------------------------------------
# Name:        dashboard.app
# Purpose:     Provides operational data dashboard for Colorado College's
#              Library Systems.
#
# Author:      Jeremy Nelson
#
# Created:     2014/06/24
# Copyright:   (c) Jeremy Nelson, Colorado College 2014
# Licence:     MIT
#-------------------------------------------------------------------------------
__version__= (0,0,1)
import json
import os
import urllib2
from flask import abort, Flask, render_template, url_for

dashboard = Flask(__name__)

virtual_machines = json.load(open('../virtual-machines.json'))

@dashboard.route('/analytics')
def analytics():
    return render_template(
        'analytics.html',
        page='analytics')


@dashboard.route('/export')
def export():
    return render_template(
        'export.html',
        page='analytics')

@dashboard.route('/reports')
def reports():
    return render_template(
        'reports.html',
        page='reports')

@dashboard.route('/status/<name>')
def vm_status(name):
    status = None
    for row in virtual_machines:
        if name == row.get('name'):
            try:
                vm_response = urllib2.urlopen("http://{}".format(row.get('ip4')))
                print("Success!!")
                if vm_response.code < 300:
                    status = {
                        'img': url_for('static', filename='img/success.png'),
                        'msg': 'Operational'}
                elif vm_response.code < 400:
                    status = {
                        'img': url_for('static', filename='img/caution.png'),
                        'msg': 'Caution for {}'.format(row.get('ip4'))}
                else:
                    status = {
                        'img': url_for('static', filename='img/failure.png'),
                        'msg': 'Failure for {}'.format(row.get('ip4'))}
            except urllib2.URLError:
                status = {
                    'img': url_for('static', filename='img/failure.png'),
                    'msg': 'Failure for {}'.format(row.get('ip4'))}
    if status is None:
        raise abort(404)
    return json.dumps(status)



@dashboard.route('/dashboard')
@dashboard.route('/')
def index():
    return render_template(
        'index.html',
        page='dashboard',
        virtual_machines=virtual_machines)

def main():
    dashboard.run(
        host='0.0.0.0',
        port=10001,
        debug=True)

if __name__ == '__main__':
    main()
