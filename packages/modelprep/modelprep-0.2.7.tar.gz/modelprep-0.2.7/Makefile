.PHONY: install clean build develop test test-cli lint format help release

# Python interpreter to use
PYTHON := python3
VENV := venv

help:
	@echo "Available commands:"
	@echo "make install    - Install the package and dependencies"
	@echo "make develop   - Install the package in development mode"
	@echo "make clean     - Clean up build artifacts and virtual environment"
	@echo "make build     - Build the package"
	@echo "make test      - Run tests"
	@echo "make lint      - Run linting checks"
	@echo "make format    - Format code using black and isort"
	@echo "make venv      - Create virtual environment"
	@echo "make release   - Manage releases"

venv:
	$(PYTHON) -m venv $(VENV)
	. $(VENV)/bin/activate && \
	pip install --upgrade pip setuptools wheel

install: venv
	. $(VENV)/bin/activate && \
	pip install .

develop: venv
	. $(VENV)/bin/activate && \
	pip install -e . && \
	pip install -r requirements.txt

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf $(VENV)
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) -m build

install-test:
	pip install -e ".[test]"

test: install-test
	pytest tests/ -v --cov=modelprep

lint: develop
	. $(VENV)/bin/activate && \
	pylint src/modelprep

format: develop
	. $(VENV)/bin/activate && \
	black src/modelprep tests && \
	isort src/modelprep tests

test-ci:
	pytest tests/ -v --cov=modelprep --cov-report=xml

release:
	@echo "Current version: $$(git describe --tags --abbrev=0)" && \
	echo "\nLast 5 releases:" && \
	git tag -l "v*" --sort=-v:refname | head -n 5 && \
	LATEST_TAG=$$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0") && \
	MAJOR=$$(echo $$LATEST_TAG | cut -d. -f1 | tr -d 'v') && \
	MINOR=$$(echo $$LATEST_TAG | cut -d. -f2) && \
	PATCH=$$(echo $$LATEST_TAG | cut -d. -f3) && \
	NEXT_PATCH="$$MAJOR.$$MINOR.$$((PATCH + 1))" && \
	NEXT_MINOR="$$MAJOR.$$((MINOR + 1)).0" && \
	NEXT_MAJOR="$$((MAJOR + 1)).0.0" && \
	echo "\nSuggested versions:" && \
	echo "Patch: $$NEXT_PATCH (for bug fixes)" && \
	echo "Minor: $$NEXT_MINOR (for new features)" && \
	echo "Major: $$NEXT_MAJOR (for breaking changes)" && \
	echo "\nEnter new version: " && read VERSION && \
	if [ -n "$$VERSION" ]; then \
		echo "\nCreating release v$$VERSION..." && \
		echo "Release notes (end with Ctrl+D):" && \
		NOTES=$$(cat) && \
		git tag -a "v$$VERSION" -m "Release v$$VERSION" -m "$$NOTES" && \
		git push origin "v$$VERSION" && \
		echo "\n[✓] Release v$$VERSION created and pushed!" && \
		echo "[✓] GitHub Actions will now build and publish to PyPI"; \
	else \
		echo "Release cancelled"; \
	fi