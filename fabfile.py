from fabric.api import *
import fabric.contrib.project as project
import os
import shutil
import sys
import SocketServer

from pelican.server import ComplexHTTPRequestHandler

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'vagrant@localhost:22'
dest_path = '/www/sjudeu.sk'

# Port for `serve`
PORT = 8080

def clean():
    """Remove generated files"""
    if os.path.isdir(DEPLOY_PATH):
        shutil.rmtree(DEPLOY_PATH)
        os.makedirs(DEPLOY_PATH)

def build():
    """Build local version of site"""
    local('pelican -s pelicanconf.py')

def rebuild():
    """`clean` then `build`"""
    clean()
    build()

def regenerate():
    """Automatically regenerate site upon file modification"""
    local('pelican -r -s pelicanconf.py')

def serve():
    """Serve site at http://localhost:8080/"""
    os.chdir(env.deploy_path)

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()

def reserve():
    """`build`, then `serve`"""
    build()
    serve()

def preview():
    """Build production version of site"""
    local('pelican -s publishconf.py')

def local_publish(environment):
    """Publish to local folders via rsync"""
    if environment == "publish":
        local('pelican -s publishconf.py')
    elif environment == "local":
        local('pelican -s testconf.py')
    cmd = 'rsync --delete --exclude ".DS_Store" -pthrvz -c {}/ {}'.format(
            DEPLOY_PATH.rstrip('/') + '/',
            dest_path
            )
    local(cmd)


@hosts(production)
def publish(environment):
    """Publish to production via rsync"""
    if environment == "publish":
        local('pelican -s publishconf.py')
    elif environment == "local":
        local('pelican -s testconf.py')

    project.rsync_project(
        remote_dir=dest_path,
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True,
        extra_opts='-c',
    )

