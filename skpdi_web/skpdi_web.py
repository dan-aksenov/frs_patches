import requests
from utils import colours

def check_webpage(patch_num, application_host, app_context):
    ''' Seek version name in SKPDI's web page's code. '''

    page = requests.get('http://' + application_host + ':8080/' + app_context)
    if page.status_code != 200:
       print( colours.Bcolors.WARNING + "WARNING: Application " + app_context + " on " + application_host + " is unnaccesseble: " + str(page.status_code) + "\n" + colours.Bcolors.ENDC )
    elif 'ver-' + patch_num + '.ico' in page.text:
        print( colours.Bcolors.OKGREEN + "SUCCESS: Application " + app_context + " on " + application_host + " matches " + patch_num + " version\n" + colours.Bcolors.ENDC )
    elif 'ver-' + patch_num + '.ico' not in page.text:
        print( colours.Bcolors.WARNING + "WARNING: Application " + app_context + " on " + application_host + " not matches " + patch_num + " version\n" + colours.Bcolors.ENDC )
    else:
        print( colours.Bcolors.WARNING + "WARNING: Problem determining application version for" + app_context +" on " + application_host + ".\n" + colours.Bcolors.ENDC )
