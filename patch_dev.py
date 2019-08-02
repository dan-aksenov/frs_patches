from patch_database import patch_database_only
import utils
from getopt import getopt
import sys
import os

if sys.version_info[0] < 3:
   raise Exception("Must be using Python 3!")

# Get patch number and target environment from parameters n and t
try:
    opts, args = getopt(sys.argv[1:], 'h:d:p:n:t:')
except Exception:
    print("-h database host -d database name -p directory with patches -n patch number -t for staging directory for temporary storage")
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
    elif opt in ('-t'):
        stage_dir = arg
    else:
        print("-n for patch number")
        sys.exit()

db_user = 'ods'
patch_table = 'parameter.fdc_patches_log'

d = patch_database_only.PatchDatabase(
    patch_num,
    sunny_path,
    db_host,
    db_name,
    stage_dir,
    db_user,
    patch_table
    )

d.patchdb()
