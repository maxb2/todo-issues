.DEFAULT_GOAL := help

.PHONY: help
help: ## Show help
	@echo "TODO Issues Tools"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install-deps
install-deps:
	poetry install --all-extras

.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit install

.PHONY: install
install: install-deps install-pre-commit ## Install dependencies and pre-commit

.PHONY: fmt
fmt: ## Format code
	poetry run bash -c 'isort . && black .'

.PHONY: lint
lint: ## Lint code
	poetry run black --check todo_issues
	poetry run ruff todo_issues

.PHONY: check
check: lint check-types ## Lint and type check code

.PHONY: check-types
check-types: ## Type check code
	poetry run mypy todo_issues

.PHONY: clean
clean: ## Clean project directory
	find . | grep -E "(/__pycache__$$|\.pyc$$|\.pyo$$)" | xargs rm -rf
	rm -rf dist .pytest_cache .mypy_cache .ruff_cache site


.PHONY: test
test: ## Test code
	poetry run pytest --cov=todo_issues --cov-report=xml

.PHONY: all
all: install fmt check test ## Install, format, lint, type-check, and test code
