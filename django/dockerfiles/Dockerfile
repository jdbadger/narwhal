ARG PYTHON_VERSION=3.11.6
FROM python:$PYTHON_VERSION-slim as base

#--BUILDER-#

FROM base as builder

# install system dependencies
# RUN apt update && \
#     apt install -y --no-install-recommends \
#     ---add packages here--- \
#     && rm -rf /var/lib/apt/lists/*

# set python environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install packages into virtual environment
COPY requirements /requirements
RUN python3 -m venv /venv
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -r /requirements/core.pip

#--FINAL--#

FROM base as final

# install system dependencies
# RUN apt update && \
#     apt install -y --no-install-recommends \
#     ---add packages here--- \
#     && rm -rf /var/lib/apt/lists/*

ARG UNAME
ARG UID

# create directory for the app user
RUN mkdir -p /home/$UNAME

# create the app user
RUN addgroup --system $UNAME --gid $UID \
    && adduser --system --ingroup $UNAME --uid $UID --shell /bin/bash $UNAME

# create the appropriate directories
ENV HOME=/home/$UNAME
ENV APP_HOME=$HOME/code
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# set python env
ENV PYTHONPATH=$HOME/code
ENV PYTHONUNBUFFERED 1

# copy project
COPY . $APP_HOME

# copy venv from builder
COPY --from=builder /venv /venv
ENV PATH=/venv/bin:$PATH

# make entrypoint script executable 
RUN chmod +x  $APP_HOME/entrypoint.sh

# chown all the files to the app user
RUN chown -R ${UNAME}:${UNAME} $HOME

# switch to app user
USER $UNAME