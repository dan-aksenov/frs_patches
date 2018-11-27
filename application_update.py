import sys
import json
import os
from glob import glob
from utils import Deal_with_linux, Bcolors
from time import sleep

class ApplicationUpdate:
    def __init__( self, jump_host, patch_num, sunny_path, application_hosts, application_path, tomcat_name, ansible_inventory, wars, update_online=None ):
        # intermediate host with ansible installation.
        self.jump_host = jump_host
        self.patch_num = patch_num
        self.sunny_path = sunny_path
        self.sunny_patch = sunny_path + patch_num + '/'
        # application hosts as writen in ansible invenrory
        self.application_hosts = application_hosts
        self.application_path = application_path
        self.tomcat_name = tomcat_name
        self.ansible_inventory = ansible_inventory
        self.ansible_cmd_template = 'ansible -i ' + ansible_inventory + ' '
        # war files mappings. example [ 'pts-integration-' + patch_num + '.war', 'integration' ].
        self.wars = wars
        if update_online is None:
            update_online = False
        self.update_online = update_online
        self.linux = Deal_with_linux()
            
    def get_ansible_result( self, paramiko_result ):
        ''' Convert ansible-paramiko result(string) to json '''
        
        a = paramiko_result
        #ansible_result = json.loads(a[a.find("{"):a.find("}")+1])
        # upper string works incorrectly with multiple nested {}. Not shure if we need to propper terminate on last }?
        try:
            ansible_result = json.loads(a[a.find("{"):])
        except:
            print( Bcolors.FAIL + 'ERROR: ' + paramiko_result + ' ' + Bcolors.ENDC )
        return ansible_result
    
    def deal_with_tomcat( self, application_host, tomcat_name, tomcat_state ):
        ''' Start/stop tomcat application server
        variables:
           - tomcat_name is systemd service name
           - tomcat_state - tomcat desired state i.e stopped, started etc. '''
    
        print "Ensuring tomcat is " + tomcat_state + "..."
        a = self.linux.linux_exec( self.jump_host, self.ansible_cmd_template + application_host + ' -m service -a "name=' + tomcat_name + ' state=' + tomcat_state + '" --become')
        ansible_result = self.get_ansible_result(a)
        if ansible_result['state'] == tomcat_state:
            print ( Bcolors.OKBLUE + "OK: Tomcat " + tomcat_state + Bcolors.ENDC )
        elif ansible_result['state'] <> tomcat_state:
            print ( Bcolors.FAIL + "FAIL: tomcat not " + tomcat_state + "!" + Bcolors.ENDC )
            sys.exit()
        else:
            print ( Bcolors.FAIL + "FAIL: Error determining tomcat state!" +  Bcolors.ENDC )
            sys.exit()

    def application_update( self ):
        ''' Update application '''
        for application_host in self.application_hosts:
            print "Checking application files on " + application_host +":"
            # apps_to_update will hold application names to be updated, so uptodate applications won't be undeployed.
            apps_to_update = []
            for war in self.wars:
                if os.path.isfile( self.sunny_patch + war[0] ) == True:
                   # check if wars on app_host = wars from sunny
                    paramiko_result = self.linux.linux_exec( self.jump_host, self.ansible_cmd_template + application_host + ' -m copy -a "src=' + self.sunny_patch + war[0] + ' dest=' + self.application_path + war[1] + '.war" --check --become --become-user=tomcat' )
                    ansible_result = self.get_ansible_result(paramiko_result)
                    # if changed add to apps_to_update list
                    if 'SUCCESS' in paramiko_result:
                        if ansible_result['changed'] == True:
                            print "\t"+ war[1] + " application needs to be updated."
                            apps_to_update.append(war)
                    elif 'FAILED' in paramiko_result:
                        print ( Bcolors.FAIL + paramiko_result + Bcolors.ENDC )
                        sys.exit()
                    else:
                        print ( Bcolors.FAIL + paramiko_result + Bcolors.ENDC )
                        sys.exit()
                else:
                    print( "\tNOTICE: Unable to find " + self.sunny_patch + war[0] + ". Assume it's not required." )
            if apps_to_update == []:
                print ( Bcolors.OKGREEN + "\tApplications version on "+ application_host +" already " + self.patch_num + Bcolors.ENDC )
                sys.exit()
            elif not apps_to_update == []:
                if self.update_online == False:
                    self.deal_with_tomcat( application_host, 'tomcat', 'stopped' )
                else:
                    print( "NOTICE: Application will be updated online..." )
                for war in apps_to_update:
                    # Remove deployed folders.
                    if self.update_online == False:
                        paramiko_result = self.linux.linux_exec( self.jump_host, self.ansible_cmd_template + application_host + ' -m file -a "path=' + self.application_path + war[1] + ' state=absent" --become' )
                    # Perform war copy.
                    print "Attempt to copy "+ war[1] + " to " + application_host + "..."
                    paramiko_result = self.linux.linux_exec( self.jump_host, self.ansible_cmd_template + application_host + ' -m copy -a "src='  + self.sunny_patch + war[0] + ' dest=' + self.application_path + war[1] + '.war" --become --become-user=tomcat' )
                    if 'SUCCESS' in paramiko_result:
                        print "\tSuccesfully updated application " + war[1] + " on " + application_host
                        print "Waiting 30 seconds for application to (re)deploy..."
                        sleep(30)
                    else:
                        print ( Bcolors.FAIL + paramiko_result + Bcolors.ENDC )
                        sys.exit
                # need to variablize tomcat service name
                # Ensure tomcat is started.
                self.deal_with_tomcat( application_host, 'tomcat', 'started' )
                if self.update_online == False:
                    print "Waiting 30 seconds for application to (re)deploy..."
                    sleep(30)
            else:
                print "Something else"