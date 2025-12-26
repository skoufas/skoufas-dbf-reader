FROM docker.io/library/debian:trixie-slim

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    ca-certificates \
    git \
    openssh-client \
    zsh \
    2>&1

RUN groupadd --gid 1000 vscode \
    && useradd --uid 1000 --gid 1000 -s /bin/zsh -m vscode \
    && mkdir -p /run/user/1000 \
    && touch /home/vscode/.zshrc

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# RUN git init . && pre-commit install-hooks
