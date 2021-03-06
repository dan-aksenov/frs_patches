import sys
import os
from utils import linux, colours 
from time import sleep

class ApplicationUpdate:
    def __init__( self, jump_host, patch_num, sunny_path, application_hosts, application_path, tomcat_name, ansible_inventory, wars ):
        self.jump_host = jump_host
        self.patch_num = patch_num
        self.sunny_path = sunny_path
        self.sunny_patch = sunny_path + patch_num + '/'
        # application hosts as writen in ansible invenrory
        self.application_hosts = application_hosts
        self.application_path = application_path
        self.tomcat_name = tomcat_name
        self.ansible_inventory = ansible_inventory
        # war files mappings. example [ 'pts-integration-' + patch_num + '.war', 'integration' ].
        self.wars = wars
        self.linux = linux.Deal_with_linux( ansible_inventory )

    def application_update( self ):
        ''' Update application '''
        for application_host in self.application_hosts:
            print( "Checking application files on " + application_host +":" )
            # apps_to_update will hold application names to be updated, so uptodate applications won't be undeployed.
            apps_to_update = []
            for war in self.wars:
                if os.path.isfile( self.sunny_patch + war[0] ) == True:
                   # check if wars on app_host = wars from sunny
                    paramiko_result = self.linux.linux_exec( self.jump_host, self.linux.ansible_cmd_template + application_host + ' -m copy -a "src=' + self.sunny_patch + war[0] + ' dest=' + self.application_path + war[1] + '.war" --check --become --become-user=tomcat' )
                    # if changed add to apps_to_update list
                    if 'CHANGED' in paramiko_result:
                        print( "\t"+ war[1] + " application needs to be updated." )
                        apps_to_update.append(war)
                    elif 'SUCCESS' in paramiko_result:
                        pass
                    elif 'FAILED' in paramiko_result:
                        print ( colours.Bcolors.FAIL + paramiko_result + colours.Bcolors.ENDC )
                        sys.exit()
                    else:
                        print ( colours.Bcolors.FAIL + paramiko_result + colours.Bcolors.ENDC )
                        sys.exit()
                else:
                    print( "\tNOTICE: Unable to find " + self.sunny_patch + war[0] + ". Assume it's not required." )
            if apps_to_update == []:
                print ( colours.Bcolors.OKGREEN + "\tApplications version on "+ application_host +" already " + self.patch_num + colours.Bcolors.ENDC )
                #sys.exit()
            elif not apps_to_update == []:
                self.linux.deal_with_tomcat( application_host, 'tomcat', 'stopped' )
                for war in apps_to_update:
                    # Remove deployed folders.
                    paramiko_result = self.linux.linux_exec( self.jump_host, self.linux.ansible_cmd_template + application_host + ' -m file -a "path=' + self.application_path + war[1] + ' state=absent" --become' )
                    # Perform war copy.
                    print( "Attempt to copy "+ war[1] + " to " + application_host + "..." )
                    paramiko_result = self.linux.linux_exec( self.jump_host, self.linux.ansible_cmd_template + application_host + ' -m copy -a "src='  + self.sunny_patch + war[0] + ' dest=' + self.application_path + war[1] + '.war" --become --become-user=tomcat' )
                    if 'CHANGED' in paramiko_result:
                        print( "\tSuccesfully updated application " + war[1] + " on " + application_host )
                    else:
                        print ( colours.Bcolors.FAIL + paramiko_result + colours.Bcolors.ENDC )
                        sys.exit
                # need to variablize tomcat service name
                # Ensure tomcat is started.
                self.linux.deal_with_tomcat( application_host, 'tomcat', 'started' )
                print( "Waiting 60 seconds for application to (re)deploy..." )
                sleep(60)
            else:
                print( "Something wrong with apps_to_update variable" )
                sys.exit()
