# for args and exit and os stuff
import os
import shutil
# for file md5s
import hashlib

def md5_check(checked_file):
    ''' *.war file md5 check 
    >>> md5_check( '/etc/hosts' )
    '52ba68c508dd6249de445291720eb96f'
    '''
    
    md5sum = hashlib.md5(open(checked_file,'rb').read()).hexdigest()
    return md5sum

def recreate_dir(dir_name):
    ''' Recreate Windows directory '''
    
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    else:
        os.makedirs(dir_name)
