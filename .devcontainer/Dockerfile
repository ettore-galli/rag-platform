# Base image
FROM ubuntu:22.04 AS base

# Avoid interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Set locale to avoid warnings
RUN apt-get update && apt-get install -y locales && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Install tools and dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    lsb-release \
    software-properties-common \
    wget \
    git \
    make \
    sudo \
    zstd 

RUN apt-get install -y --no-install-recommends \
        libatomic1
        
# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

FROM base AS python-image

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

FROM python-image AS rag-image

# Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh