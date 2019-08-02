# Fors patching scripts.

## Notes for running patch_database_only

### Prerequesites

* python 3 !

Following python modules also required (might need to install them manually via pip install):

* sys,
* os,
* shutil,
* paramiko,
* hashlib,
* psycopg2,
* glob,
* getopt,
* time,
* termcolor,
* subprocess,
* re,
* requests

### Patch start example

  parameters 1 - database host, 2 - database name, 3 - directory with pathes 4 - patch number

   ``` cmd
   patch_db_only.bat mo-ghkh-dev dba_test //sunny/builds/odsxp/ 3.8.6.1
   ```

* database passwords should be supplied via pgpass ( on windows %HOME%\AppData\Roaming\postgresql\pgpass.conf, but might be elsewhere).
* simple execution in python:

   ``` python
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
   ```

### Class attributes

* patch_num - target application version(i.e. 3.6.8)
* db_host - database host 
* db_name - database name (i.e. ods_prod)
* db_user - database user to install patches (usually - ods)
* stage_dir - local writable directory to hold patches during installation (i.e. c:/tmp/patches). This directory will be droped and recreated during installation!
* sunny_path - project repository to retreive patches from.
* patch_table - set it = parameter.fdc_patches_log for skpdi
