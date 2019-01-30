import os
from pathlib import Path

from invoke import task

@task
def build(c):
    """Builds the local Pelican blog."""
    c.run('echo "Publishing your Pelican website"')
    c.run(f'pelican content -s pelicanconf.py')

@task
def publish(c):
    """Builds the Pelican blog with deployment settings."""
    c.run('echo "Building your Pelican website"')
    c.run(f'pelican content -s publishconf.py')

@task
def autoreload(c):
    """Starts the autoreload server to help during writing of blog articles."""
    c.run('echo "Running autoreload server. Press CTRL+C to stop"')
    c.run(f'pelican -r content -s pelicanconf.py')

@task
def runserver(c):
    """Starts the dev server to visualize the articles locally in a web browser 
    at url http://localhost:8000.
    """
    c.run('echo "Running development server. Press CTRL+C to stop"')
    c.run(f'python -m http.server -d output')

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
