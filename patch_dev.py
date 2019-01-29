from patch_database_only import PatchDatabase
import utils

from getopt import getopt
import sys
import os

# Get patch number and target environment from parameters n and t
try:
    opts, args = getopt(sys.argv[1:], 'h:d:p:n:')
except Exception:
    print("-h database host -d database name -p directory with patches -n patch number")
    sys.exit()

for opt, arg in opts:
    if opt in ('-h'):
        db_host = arg
    elif opt in ('-d'):
        db_name = arg
    elif opt in ('-p'):
        sunny_path = arg
    elif opt in ('-n'):
        patch_num = arg
    else:
        print("-n for patch number")
        sys.exit()

db_user = 'ods'
patch_table = 'parameter.fdc_patches_log'
stage_dir = 'c:/tmp/skpdi_patch_test'

d = PatchDatabase(
    patch_num,
    sunny_path,
    db_host,
    db_name,
    stage_dir,
    db_user,
    patch_table
    )

d.patchdb()