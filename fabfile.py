#!/user/bin/env python
#encoding:utf-8
import logging
from cuisine import mode_sudo
from fabric.api import *
from fabric.operations import sudo

logging.basicConfig()

env.hosts = ['ubuntu@115.231.94.159:22']
env.password = 'hpgolf@'

def update():
    local('cd .')
    local('sudo git add -A')
    local('sudo git commit -m "update"')
    local('sudo git push origin master')
    
def update_server():
    with mode_sudo():
        with cd('/data/srv/honmei'):
            run('git config --global user.email "376105482@qq.com"')
            run('git config --global user.name "kevin"')
            sudo('git pull origin master')
        
