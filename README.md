# Fors patching scripts and programs.

## Notes for running patch_database_only

* database passwords should be supplied via pgpass ( on windows %HOME%\AppData\Roaming\postgresql\pgpass.conf).
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
