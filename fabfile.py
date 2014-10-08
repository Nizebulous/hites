from fabric.api import run
from fabric.api import env
from fabric.api import cd
from fabric.contrib.files import exists


env.user = 'dhites'
env.host_string = 'hites.org'
env.forward_agent = True
env.no_agent = True


REPO_DIR = '~/repositories'
HITES_REPO_DIR = '~/repositories/hites'
PROJECT_DIR = '~/flask_env'


def _setup_repo():
    run('mkdir -p %s' % REPO_DIR)
    with cd(REPO_DIR):
        run('git clone git@github.com:Nizebulous/hites.git')


def deploy():
    if not exists(HITES_REPO_DIR):
        _setup_repo()
    with cd(HITES_REPO_DIR):
        run('git fetch origin')
        run('git checkout master')
        run('git pull --rebase origin master')
    with cd(PROJECT_DIR):
        run('ln -sf %s/hites' % (HITES_REPO_DIR))
        run('touch tmp/restart.txt')
