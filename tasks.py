# -*- coding: utf-8 -*-

import os
import shutil
import sys
import datetime
from pathlib import Path

from invoke import task
from invoke.util import cd
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer

BASEDIR = (Path(__file__) / '..').resolve()
INPUTDIR = BASEDIR / 'content'
OUTPUTDIR = BASEDIR / 'output'
CONFFILE = BASEDIR / 'pelicanconf.py'
PUBLISHCONF = BASEDIR / 'publishconf.py'

PORT = 8000

PELICANOPTS = '--fatal=warnings'


@task
def clean(c):
    """Remove generated files"""
    if OUTPUTDIR.is_dir():
        shutil.rmtree(OUTPUTDIR)
        OUTPUTDIR.mkdir(parents=True, exist_ok=True)

@task
def build(c):
    """Builds the local Pelican blog"""
    c.run('echo "Building your Pelican website"')
    c.run(f'pelican {INPUTDIR} -o {OUTPUTDIR} -s {CONFFILE} {PELICANOPTS}')

@task
def rebuild(c):
    """`build` with the delete switch"""
    c.run('echo "Re-building your Pelican website"')
    c.run(f'pelican -d -s {CONFFILE} {PELICANOPTS}')

@task
def publish(c):
    """Builds the Pelican blog with deployment settings"""
    c.run('echo "Publishing your Pelican website"')
    c.run(f'pelican {INPUTDIR} -o {OUTPUTDIR} -s {PUBLISHCONF} {PELICANOPTS}')

@task
def autoreload(c):
    """Starts the autoreload server to help during writing of blog articles"""
    c.run('echo "Running autoreload server. Press CTRL+C to stop"')
    c.run(f'pelican -r {INPUTDIR} -o {OUTPUTDIR} -s {CONFFILE} {PELICANOPTS}')

@task
def regenerate(c):
    """Starts the autoreload server to help during writing of blog articles"""
    autoreload(c)

@task
def serve(c):
    """Serve site at http://localhost:8000/"""

    class AddressReuseTCPServer(RootedHTTPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(
        OUTPUTDIR,
        ('', PORT),
        ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {port} ...\n'.format(port=PORT))
    server.serve_forever()

@task
def runserver(c):
    """Serve site at http://localhost:8000/"""
    serve(c)

@task
def devserver(c):
    """Starts the devserver"""
    c.run('echo "Running Pelican DevServer. Press CTRL+C to stop"')
    c.run(f'pelican -lr {INPUTDIR} -o {OUTPUTDIR} -s {CONFFILE} {PELICANOPTS} -p {PORT}')

@task
def reserve(c):
    """`build`, then `serve`"""
    build(c)
    serve(c)

@task
def preview(c):
    """Build production version of site"""
    c.run('pelican -s publishconf.py')

@task
def revert(c):
    """Reverts the repository to the previous commit if not on a Pull Request
    on Travis.
    """
    if not os.getenv('TRAVIS_PULL_REQUEST'):
        c.run('echo "Build errors were encountered. Reverting last commit..."')
        c.run('git revert HEAD -n') 
        c.run('git commit -m "Revert to last commit because errors were found."')
        c.run('git checkout -b errors')
        c.run(f'git push -f https://{GITHUB_TOKEN}@github.com/PythonClassmates/PythonClassmates.org.git errors:master') 
        c.run('echo "Last commit reverted"')
    else:
	    c.run('echo "In a pull request. Nothing to revert."') 
