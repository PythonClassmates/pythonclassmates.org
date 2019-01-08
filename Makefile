THEME=-t theme/active

publish:
	pelican content --fatal=warnings -s publishconf.py $(THEME)

build:
	pelican content --fatal=warnings -s pelicanconf.py $(THEME)

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
