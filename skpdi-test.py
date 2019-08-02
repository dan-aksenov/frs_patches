from application_update import application_update
from patch_database import patch_database
import utils
from skpdi_web import skpdi_web

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
application_hosts = ['cos7-sb2']
# // so windows can also read in correctly
sunny_path = '/sunny/builds/odsxp/'
application_path = '/opt/tomcat/webapps/'
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
#update_online = True

d = patch_database.PatchDatabase(
    jump_host,
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

a = application_update.ApplicationUpdate(
    jump_host,
    patch_num,
    sunny_path,
    application_hosts,
    application_path,
    tomcat_name,
    ansible_inventory,
    wars
    )

a.application_update()

print("Chekcking application version:")
for host in application_hosts:
    for app in wars:
        skpdi_web.check_webpage(patch_num, host, app[1])
