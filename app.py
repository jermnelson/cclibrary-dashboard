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
from flask import abort, Flask, render_template

dashboard = Flask(__name__)

@dashboard.route('/analytics')
def analytics():
    return "In analytics"


@dashboard.route('/export')
def export():
    return "In export"

@dashboard.route('/reports')
def reports():
    return "In reports"

@dashboard.route('/')
def index():
    return render_template(
        'index.html',
        page='dashboard')

def main():
    dashboard.run(
        host='0.0.0.0',
        port=10001,
        debug=True)

if __name__ == '__main__':
    main()
