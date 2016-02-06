#!/usr/bin/python2.7 -tt

### code challenge ###
# by Christopher Harty
# Feb. 2, 2016
#
#
# DISCLAIMER:
# 1. Please do not deploy this into a production environment
# 2. The below python code has been created from the scope of
#    a challenge.  A time constraint also played apart with
#    what could actually be accomplished.
######################

import subprocess
import sys


### Usage: edit the main() function at the bottom ###

"""
====>Updates:
 - fabric option
 - ansible option
 - service option using raw_input to allow for meta input
 - initial optparse options
 - yaml config option
 - logging

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
===>Challenge:
Create a Python script that can do the following:
  1. SSH into a remote environment
  2. Create the directory to store the application code
  3. Git clone a repo into an application directory
  4. Start up the server from the cloned application

Conditions:
  1. The script should be able to report on failures on any step
  2. The script should start up a Rails server (command: "bundle exec rails s production") in the background
  3. Assume that the remote host already has the SSH keys necessary to pull from the repo
  4. The script should report which step it is on during each step of the process

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

====>Assumptions:
We will run the script from a local environment against a test VM to verify results.
For this challenge I am assuming the following:
 - a VM with Ubuntu 12.*, 13.*, or 14.* is up
 - credentials for ssh, git, and sudo are already setup
 - a working rails environment is already setup.
 - git is installed
 - python 2.7.* is installed


====>Notes:
 - The possible solutions below could of course be enhanced 
   with option parsing, raw_input, or abstracted into an api.
 - Under the current constraints there are many options, but
   only a couple of tasty ones.  I have listed several possibilities and
   expanded a couple of them.  The correct solution will depend on the
   full scope of the environment.
 - I would probably consider sockets or proto buffers for a really futuristic 
   solution :)  Also, in a permanent solution I would add python's logging feature.
 - I realize there are better 3rd party libraries for performing some
   tasks, however I opted for straight python code, since that was what was asked for.
   Fabric and Ansible would however be my answer (in python) to this problem, if I could 
   use third party solutions. 
 - Finally, I chose functional instead of objects and/or generators as the maturity level of
   this tool does not warrant it as of yet.
"""
        

class TestCases(object):

    def test_py_cmds(self):
        target_dir = '/home/ubuntu/app4'
        repo = 'https://github.com/joshmcarthur/inquest.git'
        return [
            ('Remove previous attempts', 'import subprocess; subprocess.check_output(["bash","-c","rm -rf %s"])' % target_dir),
            ('Create directory', 'import os; os.mkdir("%s")' % target_dir),
            ('Directory exists?', 'import os; print os.path.exists("%s")' % target_dir),
            ('Cloning repository', 'import subprocess; print subprocess.check_output(["bash","-c","git clone %s %s"])' % (repo, target_dir)),
            #('Starting background rails service', 'import subprocess; subprocess.check_output(["bash","-c","cd %s; /usr/bin/nohup /home/ubuntu/.rbenv/versions/2.2.3/bin/ruby bin/rails s -e production --binding=172.30.0.85 &>/dev/null &"])' % target_dir),
            ('Starting background rails service', 'import subprocess; print subprocess.check_output(["bash","-c","cd %s; /home/ubuntu/.rbenv/versions/2.2.3/bin/ruby bin/rails s -e production --binding=172.30.0.85 &>/dev/null &"])' % target_dir),
            ('ps augfx', 'import subprocess; res=subprocess.check_output(["bash","-c","ps augfx | grep \'rail\'"]); print str(res)'),
            ('Hostname', 'import socket; print socket.gethostname()'),
            ('Get current working directory', 'import os; print os.getcwd()'),
            ('Error example for IP', 'import socket; print socket.gethostbyname(socket.gethostname())'),
            ]

    def test_sh_cmds(self):
        target_dir = '/home/ubuntu/app4'
        repo = 'https://github.com/joshmcarthur/inquest.git'
        return [
            ('Remove previous attempts', 'rm -rf %s' % target_dir),
            ('Create directory', 'mkdir %s' % target_dir),
            ('Directory exists?', 'if [ -d "%s" ]; then echo "Directory exists."; else echo "Directory does not exist."; fi' % target_dir),
            ('Cloning repository', 'git clone %s %s' % (repo, target_dir)),
            ('Starting background rails service', 'cd %s; /home/ubuntu/.rbenv/versions/2.2.3/bin/ruby bin/rails s -e production --binding=172.30.0.85 &>/dev/null & \ ' % target_dir),
            ('ps augfx', 'ps augfx | grep "rail"'),
            #('Get current working directory', 'pwd'),
            #('Hostname', 'uname -a'),
            #('Error example for unames', 'unames'),
            ]


        

class DevCases(object):
    """delivers templated command lists for py and sh."""

    def __init__(self, script, target_dir, repo):
        self.script = script
        self.target_dir = target_dir
        self.repo = repo

    def get_commands(self):
        if self.script == "py":
            return self.py_commands()
        elif self.script == "sh":
            return self.sh_commands()

    def py_commands(self):
        return [
            ('Remove previous attempts', 'import subprocess; subprocess.check_output(["bash","-c","rm -rf %s"])' % self.target_dir),
            ('Create directory', 'import os; os.mkdir("%s")' % self.target_dir),
            ('Directory exists?', 'import os; print os.path.exists("%s")' % self.target_dir),
            ('Cloning repository', 'import subprocess; print subprocess.check_output(["bash","-c","git clone %s %s"])' % (self.repo, self.target_dir)),
            ('Starting background rails service', 'import subprocess; print subprocess.check_output(["bash","-c","cd %s; /home/ubuntu/.rbenv/versions/2.2.3/bin/ruby bin/rails s -e production --binding=172.30.0.85 &>/dev/null &"])' % self.target_dir),
            ('ps augfx', 'import subprocess; res=subprocess.check_output(["bash","-c","ps augfx | grep \'rail\'"]); print str(res)'),
            ]

    def sh_commands(self):
        return [
            ('Remove previous attempts', 'rm -rf %s' % self.target_dir),
            ('Create directory', 'mkdir %s' % self.target_dir),
            ('Directory exists?', 'if [ -d "%s" ]; then echo "Directory exists."; else echo "Directory does not exist."; fi' % self.target_dir),
            ('Cloning repository', 'git clone %s %s' % (self.repo, self.target_dir)),
            ('Starting background rails service', 'cd %s; /home/ubuntu/.rbenv/versions/2.2.3/bin/ruby bin/rails s -e production --binding=172.30.0.85 &>/dev/null & \ ' % self.target_dir),
            ('ps augfx', 'ps augfx | grep "rail"'),
            ]
        

class PopenOSError(OSError):
        """Popen: OSError."""

        
class PopenArgumentError(ValueError):
        """Popen: Invalid arguments."""

        
class RemoteControl(TestCases):
    """
    support bash and python commands.
    support script params and input for host and commands
    """

    DEBUG = True
    TEST_MODE = True
    HOST = ""
    TOOL = ""
    commands = []
    COMMAND = ""
    script_available = ['py','sh']
    script = ""

    def __init__(self, host, script="sh", commands=None, debug=True, test_mode=True):
        """
        Input:
        - host: (str) qualified domain name or ip address
        - commands: (str) commands to be send via ssh
        """
        super(self.__class__, self).__init__()
        
        self.script = script
        self.DEBUG = debug
        self.TEST_MODE = test_mode
        
        self.HOST = "%s" % str(host)

        if test_mode:
            if self.script == 'py':
                commands = self.test_py_cmds()
            elif self.script == 'sh':
                commands = self.test_sh_cmds()
                
        if commands:
            if isinstance(commands, list):
                self.commands.extend(commands )
            elif isinstance(commands, tuple):
                self.commands.extend(commands[:])
            
        self.repackage_commands()

        self.logger.info('Init is complete.')

    def add_command(self, description, command):
        """Add a python command to the list to be sent to another host."""
        
        self.commands.append((description, command))
        self.repackage_commands()

    def repackage_commands(self):
        if self.script == "py":
            self._repackage_py_commands()
        elif self.script == "sh":
            self._repackage_sh_commands()

    def _repackage_py_commands(self):
        """Repackage commands a bit into a string of chained commands."""
        
        command_chain = ';'.join([ 'print; print "### '+cmd[0]+':"; '+cmd[1] for cmd in self.commands ])
        self.COMMAND = """python -c '%s'""" % command_chain
        if self.DEBUG: print 'py command chain: %s' % self.COMMAND
        

    def _repackage_sh_commands(self):
        """Repackage commands a bit into a string of chained commands.

        Note: I chose to use ';' instead of '&&' between commands
        so that all output could be witnessed at once.  In Production
        this would probably be a different case.  Addtionally, there might
        some speed boosts if I were to group some commands, but would need
        make sure that all commands remained in order.
        """
        
        command_chain = '; '.join([ "echo; echo '### "+cmd[0]+" (command: "+cmd[1]+"):'; "+cmd[1] for cmd in self.commands ])
        self.COMMAND = command_chain
        if self.DEBUG: print 'sh command chain: %s' % self.COMMAND

    def send_request(self):
        
        if self.HOST and self.COMMAND:
            self._send_via_ssh()

        print '\nProcess completed.\n'

    def _send_via_ssh(self):
        """A function that sends commands via ssh.
        
        Return: False if Error else True
        """
        
        # setup variables
        self.TOOL = "ssh"

        args = [self.TOOL, self.HOST, self.COMMAND]
        
        if self.DEBUG: print """
################
###### args ####
%s
################
""" % str(args)
        
        try:
            # send request
            ssh = subprocess.Popen(
                args,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            response, error = ssh.communicate()
            
            if self.DEBUG: print """
################
#### errors ####
%s
################
""" % str(error)

            print '\nresponse:'
            print response
            
            if error:
                error_msg = """
-----------------------------------
>>> REMOTE COMMAND ERRORS <<<
  - %s
-----------------------------------
""" % str(error)

                if 'cloning into' in error.lower():
                    print error_msg.replace('Cloning into', 'Warning Only: Cloning into')

                else:
                    print >>sys.stderr, error_msg

        except OSError:
            raise PopenOSError()

        except ValueError:
            raise PopenArgumentError(','.join(args))



def main():
    """Please edit the RemoteControl params as needed.

    Connection and processing variables:
     - debug: (bool) will print additional information about the process.
     - test_mode: (bool) will only work off of TestCases() methods.
     - target_host: (str) typically ssh-config hostname entry.
     - script: (str) what environment should these requests be evaluated in?
       Current options: ["sh","py"], possible future options ["fabric", "perhaps ansible"]
     
    Command variables:
     - target_dir: (str) # target directory on remote box.
     - repo: (str) url for a git repository.
     - commands: (list) a ordered sequence of commands to be run.

    """
    
    # connection and processing variables
    debug = False
    test_mode = False
    target_host = 'rails'
    script="py" # "sh" or "py"

    # command variables
    target_dir = '/home/ubuntu/app/' 
    repo = 'https://github.com/joshmcarthur/inquest.git'
    dev = DevCases(script, target_dir, repo)
    commands = dev.get_commands()

    rc = RemoteControl(target_host,script,commands,debug,test_mode)
    rc.send_request()

if __name__ == "__main__":
    main()
