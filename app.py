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
import ansible.runner

runner = ansible.runner.Runner(
  module_name='ping',
  module_args='',
  pattern='DMZ',
  forks=10
)

datastructure = runner.run()
print(datastructure)

dashboard = Flask(__name__)

services = json.load(open('../services.json'))
virtual_machines = json.load(open('../virtual-machines.json'))

def add_service():
    service = dict()
    service['name'] = input("Service Name:")
    print("Library VMs")
    for i,vm in enumerate(lib_vms):
        print("{} - {}".format(i, vm.get('name')))
    vm_num = input("Select number >>")
    if int(vm_num) < 0 or int(vm_num) > len(lib_vms):
        print("Invalid choice...")
        return
    else:
        service['ip4'] = lib_vms[int(vm_num)].get('ip4')
        service['host'] = lib_vms[int(vm_num)].get('name')
    service['port'] = input("Port Number")
    service['max_memory'] = input("Max memory:")
    service['item-count'] = input("Total number of records, items, or other:")
    print("Keep: {}".format(service))
    keep = input("Y|N >>")
    if keep.lower().startswith('y'):
        services.append(service)
    continue_ = input("Continue? Y|N >>")
    if continue_.lower().startswith('y'):
        add_service()

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



@dashboard.route('/dashboard/')
@dashboard.route('/')
def index():
    return render_template(
        'index.html',
        page='dashboard',
        services=services,
        virtual_machines=virtual_machines)

def main():
    dashboard.run(
        host='0.0.0.0',
        port=10002,
        debug=True)

if __name__ == '__main__':
    main()
