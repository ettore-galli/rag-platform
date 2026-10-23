
setup-lint:
	uv tool install ruff
	uv tool install pyright
	uv tool install black

test:
	pytest -s -vvv tests/unit/

lint:
	uv run black .
	uv run ruff check .
	uv run pyright .

ruff-fix:
	uv run ruff check . --fix

sync:
	uv sync  

install-python:
	uv python install 3.12
	uv python update-shell

create:
	uv venv --clear --python python3.12 .venv 
