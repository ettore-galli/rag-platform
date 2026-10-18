# RAG PLATFORM - DEV TOOLS SETUP


## Setup uv

These are the steps to perform *once* in order to have UV installed (locally and not on your system)

```shell
export UV_INSTALL_DIR="$(pwd)/tools/uv"
curl -LsSf https://astral.sh/uv/install.sh | sh

```

```shell
export PATH="$(pwd)/tools/uv:$PATH"
```

## Init uv

```shell
uv init --no-workspace
```

```shell
uv add [a-library]
...

uv add --dev ruff
uv add --dev black
uv add --dev pyright
```
