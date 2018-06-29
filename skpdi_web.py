import requests
from utils import Bcolors

def check_webpage(patch_num, application_host, target):
    # redo it with /u01/apache-tomcat-8.5.23/webapps/record/META-INF/maven/ru.fors.ods/record/pom.xml version check?
	# cos it'll also work on pts
    ''' Seek version name in web page's code. '''

    page = requests.get('http://' + application_host + ':8080/' + target)
    if page.status_code <> 200:
       print Bcolors.WARNING + "WARNING: Application " + target + " on " + application_host + "is unnaccesseble: " + str(page.status_code) + "\n" + Bcolors.ENDC
    elif 'ver-' + patch_num + '.ico' in page.text:
        print Bcolors.OKGREEN + "SUCCESS: Application " + target + " on " + application_host + " matches " + patch_num + " version\n" + Bcolors.ENDC
    elif 'ver-' + patch_num + '.ico' not in page.text:
        print Bcolors.WARNING + "WARNING: Application " + target + " on " + application_host + " not matches " + patch_num + " version\n" + Bcolors.ENDC
    else:
        print Bcolors.WARNING + "WARNING: Problem determining application version for" + target +" on " + application_host + ".\n" + Bcolors.ENDC
