THEME=-t theme/active

publish:
	pipenv run pelican content -s publishconf.py $(THEME)

build:
	pipenv run pelican content -s pelicanconf.py $(THEME)
	
autoreload:
	pipenv run pelican -r content -s pelicanconf.py $(THEME)
	
runserver:
	pipenv run python -m http.server -d output

revert:
ifeq ($(TRAVIS_PULL_REQUEST), false)
	@echo "Build errors were encountered. Reverting last commit..."
	@git revert HEAD -n
	@git commit -m "Revert to last commit because errors were found."
	@git checkout -b errors
	@git push -f https://$(GITHUB_TOKEN)@github.com/PythonClassmates/PythonClassmates.org.git errors:master
	@echo "Last commit reverted"
else
	@echo "In a pull request. Nothing to revert."
endif

.PHONY: publish build revert
