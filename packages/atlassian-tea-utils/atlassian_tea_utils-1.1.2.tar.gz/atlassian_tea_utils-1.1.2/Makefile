DEFAULT_BRANCH := main

default: check

.PHONY: default check format test sonar unit_test_and_sonar_scan unit_test clean dist


check: clean lint test

lint:
	pipenv run flake8
	pipenv run isort --check-only .
	pipenv run black --check .
	pipenv run mypy . --show-error-codes

format:
	pipenv run isort .
	pipenv run black .

sonar:
# Add a projectVersion flag only on the main branch
# Add --checkQualityGates so the process will fail if the quality gates specified for the project has failed.
ifeq ($(BITBUCKET_BRANCH),${DEFAULT_BRANCH})
	atlas sonar scan --checkQualityGates --defaultBranch ${DEFAULT_BRANCH} --projectVersion $(BITBUCKET_BUILD_NUMBER)
else
	atlas sonar scan --checkQualityGates --defaultBranch ${DEFAULT_BRANCH}
endif

unit_test_and_sonar_scan:
	pipenv run coverage run -m pytest . -rsx -s
	pipenv run coverage xml
	make sonar

test:
	make unit_test

unit_test:
	pipenv run pytest atlassian_tea_utils tests -rsx -s

integ_test:
	pipenv run pytest atlassian_tea_utils integ_tests -rsx -s


clean:
	rm -rf atlassian_tea_utils.egg-info build dist

dist: clean
	pipenv run python -m build --wheel --sdist

