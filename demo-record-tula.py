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
except StandardError:
    print("-n for patch number")
    sys.exit()

for opt, arg in opts:
    if opt in ('-n'):
        patch_num = arg
    else:
        print("-n for patch number")
        sys.exit()

# Variables
# host to run ansible commands from
jump_host = "oemcc.fors.ru"
ansible_inventory = '~/ansible-hosts/record-tula'
# application hosts as writen in ansible invenrory
application_hosts = ['record-tula']
# // so windows can also read it correctly, same as linux
sunny_path = '/sunny/builds/odsxp/'
# tomcat application location
application_path = '/opt/tomcat/webapps/'
# sysinit or systemd service name to stop/start server
tomcat_name = 'tomcat'
# war files mappings
wars = [
    ['r71-tula-' + patch_num + '.war', 'app']
    ]

db_host = 'mo-ghkh-dev'
db_name = 'ods_tula_prod'
db_user = 'ods'
# databaes table to look for current db_version
patch_table = 'parameter.fdc_patches_log'
# temporary directory to hold database patches.
stage_dir = '/tmp/demo_tula_patch'

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

#a.application_update()

