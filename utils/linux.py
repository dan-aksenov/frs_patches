# for args and exit and os stuff
import sys
import os
import shutil
# for ssh connection and ftp transfer.
import paramiko
# to parse ansible results
import json
from . import colours

class Deal_with_linux:
    def __init__(self, ansible_inventory):
        self.linux_key_path = os.getenv('HOME') + '/.ssh/id_rsa'
        if not os.path.isfile(self.linux_key_path):
            print( colours.Bcolors.FAIL + "\nERROR: Linux ssh key not found!" + colours.Bcolors.ENDC )
            print( "HINT: Make sure \"" + self.linux_key_path + "\" exists." )
            sys.exit()

        # Prepare key for paramiko.
        self.linux_key = paramiko.RSAKey.from_private_key_file(self.linux_key_path)
        # SSH user
        self.ssh_user = 'ansible'
        # SSH port
        self.ssh_port = 22
        self.jump_host = 'oemcc.fors.ru'
        self.ansible_cmd_template = 'ansible -i ' + ansible_inventory + ' '
        self.ansible_inventory = ansible_inventory

    def linux_exec(self, linux_host, shell_command):
        ''' Linux remote execution '''
       
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=linux_host, username=self.ssh_user, port=self.ssh_port, pkey=self.linux_key)
        except:
            print( colours.Bcolors.FAIL + "\nERROR: unable to execute on Linux machine!" + colours.Bcolors.ENDC )
            sys.exit()
        stdin, stdout, stderr = client.exec_command(shell_command)
        data = (stdout.read() + stderr.read()).decode('ascii').strip("\n")
        client.close()
        return data

    def linux_put(self, linux_host, source_path, dest_path):
        ''' Copy to remote Linux '''
           
        transport = paramiko.Transport((linux_host, self.ssh_port))
        try:
            transport.connect(username=self.ssh_user, pkey=self.linux_key)
        except:
            print( colours.Bcolors.FAIL + "\nERROR: unable to copy to Linux machine!" + colours.Bcolors.ENDC )
            sys.exit()
        sftp = paramiko.SFTPClient.from_transport(transport)
    
        localpath = source_path
        remotepath = dest_path

        sftp.put(localpath, remotepath)
        sftp.close()
        transport.close()

    def linux_get(self, linux_host, source_path, dest_path):
        ''' Copy from remote Linux '''
      
        transport = paramiko.Transport((linux_host, self.ssh_port))
        try:
            transport.connect(username=self.ssh_user, pkey=self.linux_key)
        except:
            print( colours.Bcolors.FAIL + "\nERROR: unable to copy to Linux machine!" + colours.Bcolors.ENDC )
            sys.exit()
        sftp = paramiko.SFTPClient.from_transport(transport)
 
        localpath = source_path
        remotepath = dest_path

        sftp.get(localpath,remotepath)
        sftp.close()
        transport.close()

    def get_ansible_result( self, paramiko_result ):
        ''' Convert ansible-paramiko result(string) to json. Function not used right now. To be removed... '''
        
        a = paramiko_result
        #ansible_result = json.loads(a[a.find("{"):a.find("}")+1])
        # upper string works incorrectly with multiple nested {}. Not shure if we need to propper terminate on last }?
        try:
            ansible_result = json.loads(a[a.find("{"):])
        except:
            print( colours.Bcolors.FAIL + 'ERROR: ' + paramiko_result + ' ' + colours.Bcolors.ENDC )
        return ansible_result
    
    def deal_with_tomcat( self, application_host, tomcat_name, tomcat_state ):
        ''' Start/stop tomcat application server
        variables:
           - tomcat_name is systemd service name
           - tomcat_state - tomcat desired state i.e stopped, started etc. '''
    
        print( "Ensuring " + tomcat_name + " is " + tomcat_state + "..." )
        paramiko_result = self.linux_exec( self.jump_host, self.ansible_cmd_template + application_host + ' -m service -a "name=' + tomcat_name + ' state=' + tomcat_state + '" --become')
        
        if 'CHANGED' in paramiko_result:
            print( colours.Bcolors.OKBLUE + "OK: Tomcat " + tomcat_state + colours.Bcolors.ENDC )
        elif 'FAILED' in paramiko_result:
            print( colours.Bcolors.FAIL + "FAIL: Tomcat not " + tomcat_state + "!" + colours.Bcolors.ENDC )
            sys.exit()
        elif 'SUCCESS' in paramiko_result:
            print( colours.Bcolors.OKBLUE + "OK: Tomcat is already  " + tomcat_state + colours.Bcolors.ENDC )
        else:
            print( colours.Bcolors.WARNING + "Error determining tomcat state!" +  colours.Bcolors.ENDC )
            print( paramiko_result )
            sys.exit()
