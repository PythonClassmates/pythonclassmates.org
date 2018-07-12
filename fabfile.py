import os

from invoke import task

PELICAN = './env/bin/pelican'

@task
def venv(c):
    """Creates a virtualenv for the build."""
    if not os.path.exists('env/bin/pip'):
        c.run('python3 -m venv env')
    c.run('./env/bin/pip install -r requirements.txt')

@task(venv)
def build(c):
    """Builds the Pelican blog with dev configuration."""
    c.run(
        f'{PELICAN} -s pelicanconf.py '
        '--fatal=warnings content'
    )

@task(venv)
def publish(c):
    """Builds the Pelican blog with publish configuration."""
    c.run(
        f'{PELICAN} -s publishconf.py '
        '--fatal=warnings content'
    )

@task
def revert(c):
    """Reverts to previous commit."""
    if os.environ['TRAVIS_PULL_REQUEST'] == 'false':
        c.run('git revert HEAD -n')
        c.run('git commit -m "Revert to last commit because errors were found."')
        c.run('git checkout -b "errors"')
        c.run('git push -f https://${GITHUB_TOKEN}@github.com/PythonClassmates/PythonClassmates.org.git errors:master')
