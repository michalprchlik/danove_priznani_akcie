# variable used for deployment of the project
export PROJECT_NAME := growatt-471616
export REGION := europe-west1
URL_APP_ENGINE := oa.r.appspot.com

export SERVICE_ACCOUNT_EMAIL := 342310492603-compute@developer.gserviceaccount.com


test:
	podman build -t function_test --file test.containerfile --quiet .
	podman run --rm function_test

lint:
	python3 -m autoflake run.py modules
	python3 -m black --config pyproject.toml run.py modules
	python3 -m pylint run.py modules

check:
	python3 -m pip list --outdated
	python3 -m bandit --config pyproject.toml --recursive --quiet run.py
	python3 -m safety check --file requirements.txt
	python3 -m safety check --file requirements_lint.txt

