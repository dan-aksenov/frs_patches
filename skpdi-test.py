from application_update import ApplicationUpdate
from patch_database import PatchDatabase
import utils
from skpdi_web import check_webpage

from getopt import getopt
import sys
import os

# Get patch number and target environment from parameters n and t
try:
    opts, args = getopt(sys.argv[1:], 'n:')
except Exception:
    print("-n for patch number")
    sys.exit()

for opt, arg in opts:
    if opt in ('-n'):
        patch_num = arg
    else:
        print("-n for patch number")
        sys.exit()

# Variables
jump_host = "oemcc.fors.ru"
# application hosts as writen in ansible invenrory
application_hosts = ['centos7-test-1']
# // so windows can also read in correctly
sunny_path = '/sunny/builds/odsxp/'
application_path = '/opt/apache-tomcat-8.5.35/webapps/'
tomcat_name = 'tomcat'
ansible_inventory = '~/ansible-hosts/test'
wars = [
    ['skpdi-' + patch_num + '.war', 'predprod'],
    ['ext-' + patch_num + '.war', 'ext-predprod']
    ]

db_host = 'mo-ghkh-dev'
db_name = 'dba_test'
db_user = 'ods'
patch_table = 'parameter.fdc_patches_log'
stage_dir = '/tmp/skpdi_patch_test'
update_online = True

d = PatchDatabase(
    patch_num,
    sunny_path,
    application_hosts,
    ansible_inventory,
    db_host,
    db_name,
    stage_dir,
    db_user,
    patch_table
    )

d.patchdb()

a = ApplicationUpdate(
    jump_host,
    patch_num,
    sunny_path,
    application_hosts,
    application_path,
    tomcat_name,
    ansible_inventory,
    wars,
    update_online
    )

a.application_update()

print("Chekcking application version:")
for host in application_hosts:
    for app in wars:
        check_webpage(patch_num, host, app[1])
