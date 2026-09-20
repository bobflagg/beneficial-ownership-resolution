.PHONY: install test lint build-lwc eval export help

help:
	@echo "install    - uv sync (deps incl. nlr from git)"
	@echo "test       - run the test suite (integration tests skip without PG*)"
	@echo "lint       - ruff check"
	@echo "build-lwc  - build landlords_with_connections from wow_landlords (needs PG*)"
	@echo "eval       - the paired divergence report vs Who Owns What (needs PG*)"
	@echo "export     - write the person-free dataset to release/ (needs PG*)"

install:
	uv sync

test:
	uv run pytest -q

lint:
	uv run ruff check src tests

build-lwc:
	uv run python -m bor.build_lwc

eval:
	uv run python -m bor.eval.divergence

export:
	uv run python -m bor.export release
