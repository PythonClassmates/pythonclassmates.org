publish:
ifneq ($(TRAVIS_PULL_REQUEST), false)
	@echo "In a pull request..."
endif
	pelican content --fatal=warnings -s publishconf.py

.PHONY: publish build revert
