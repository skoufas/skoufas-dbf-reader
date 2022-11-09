ARG VARIANT=3-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

RUN python -m pip install --upgrade pip \
    && python -m pip install \
        pytest \
        pytest-cov \
        flit \
        pre-commit

COPY .pre-commit-config.yaml .
RUN git init . && pre-commit install-hooks

# COPY requirements.txt /tmp/pip-tmp/

# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

