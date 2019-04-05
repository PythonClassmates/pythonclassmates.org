# -*- coding: utf-8 -*-

import os
import shutil
import sys
from pathlib import Path

from invoke import task
from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer

CONFIG = {}
CONFIG['basedir'] = Path('.')
CONFIG['inputdir'] = CONFIG['basedir'] / 'content'
CONFIG['outputdir'] = CONFIG['basedir'] / 'output'
CONFIG['conffile'] = CONFIG['basedir'] / 'pelicanconf.py'
CONFIG['publishconf'] = CONFIG['basedir'] / 'publishconf.py'

CONFIG['opts'] = '--fatal=warnings'
CONFIG['port'] = 8000


@task
def clean(c):
    """Remove generated files"""
    if CONFIG['outputdir'].is_dir():
        shutil.rmtree(CONFIG['outputdir'])
        CONFIG['outputdir'].mkdir(parents=True, exist_ok=True)


@task
def build(c):
    """Builds the local Pelican blog"""
    c.run('echo "Building your Pelican website"')
    c.run('pelican {inputdir} -o {outputdir} -s {conffile} {opts}'
          .format(**CONFIG)
          )


@task
def html(c):
    """Builds the local Pelican blog"""
    build(c)


@task
def rebuild(c):
    """Builds with the delete switch"""
    c.run('echo "Re-building your Pelican website"')
    c.run('pelican -d -s {conffile} {opts}'.format(**CONFIG))


@task
def publish(c):
    """Builds the Pelican blog with deployment settings"""
    c.run('echo "Publishing your Pelican website"')
    c.run('pelican {inputdir} -o {outputdir} -s {publishconf} {opts}'
          .format(**CONFIG)
          )


@task
def autoreload(c):
    """Starts the autoreload server to help during writing of blog articles"""
    c.run('echo "Running autoreload server. Press CTRL+C to stop"')
    c.run('pelican -r {inputdir} -o {outputdir} -s {conffile} {opts}'
          .format(**CONFIG)
          )


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
        CONFIG['outputdir'],
        ('', CONFIG['port']),
        ComplexHTTPRequestHandler
    )

    sys.stderr.write('Serving on port {port} ...\n'.format(**CONFIG))
    server.serve_forever()


@task
def runserver(c):
    """Serve site at http://localhost:8000/"""
    serve(c)


@task
def reserve(c):
    """Builds, then serves"""
    build(c)
    serve(c)


@task
def preview(c):
    """Builds the production version of site"""
    c.run('pelican -s publishconf.py')


@task
def revert(c):
    """Reverts the repository to the previous commit if not on a Pull Request
    on Travis.
    """
    if not os.getenv('TRAVIS_PULL_REQUEST'):
        c.run('echo "Build errors were encountered. Reverting last commit..."')
        c.run('git revert HEAD -n')
        c.run(
            'git commit -m "Revert to last commit because errors were found."'
        )
        c.run('git checkout -b errors')
        c.run(
            'git push -f https://{GITHUB_TOKEN}@github.com/'
            'PythonClassmates/PythonClassmates.org.git errors:master'
            .format(**os.environ)
        )
        c.run('echo "Last commit reverted"')
    else:
        c.run('echo "In a pull request. Nothing to revert."')
