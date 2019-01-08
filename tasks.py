import os

from invoke import task


THEME = 'theme/active'

@task
def build(c):
    c.run('echo "Publishing your Pelican website"')
    c.run(f'pipenv run pelican content -s pelicanconf.py -t {THEME}')

@task
def publish(c):
    c.run('echo "Building your Pelican website"')
    c.run(f'pipenv run pelican content -s publishconf.py -t {THEME}')

@task
def autoreload(c):
    c.run('echo "Running autoreload server. Press CTRL+C to stop"')
    c.run(f'pipenv run pelican -r content -s pelicanconf.py -t {THEME}')

@task
def runserver(c):
    c.run('echo "Running development server. Press CTRL+C to stop"')
    c.run(f'pipenv run python -m http.server -d output')

@task
def revert(c):
    if not os.getenv('TRAVIS_PULL_REQUEST'):
        c.run('echo "Build errors were encountered. Reverting last commit..."')
        c.run('git revert HEAD -n') 
        c.run('git commit -m "Revert to last commit because errors were found."')
        c.run('git checkout -b errors')
        c.run(f'git push -f https://{GITHUB_TOKEN}@github.com/PythonClassmates/PythonClassmates.org.git errors:master') 
        c.run('echo "Last commit reverted"')
    else:
	    c.run('echo "In a pull request. Nothing to revert."') 
