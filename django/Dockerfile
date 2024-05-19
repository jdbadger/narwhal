ARG PYTHON_VERSION=3.11
FROM python:$PYTHON_VERSION-slim AS base

#--BUILDER-#

FROM base AS builder

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
ARG REQUIREMENTS
COPY requirements /requirements
RUN python3 -m venv /venv
RUN /venv/bin/pip install --upgrade pip
RUN /venv/bin/pip install -r $REQUIREMENTS

#--FINAL--#

FROM base AS final

# install system dependencies needed post-build
RUN apt update && \
    apt install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# create a non-root app user with user dir
ARG UNAME
ARG UID
ENV HOME /home/$UNAME
RUN mkdir -p $HOME
RUN addgroup --system $UNAME --gid $UID \
    && adduser --system --ingroup $UNAME --uid $UID --shell /bin/bash $UNAME

# create directory for the app
ENV APP_HOME=$HOME/code
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# copy project to app dir
COPY . $APP_HOME

# copy venv from builder and update path
COPY --from=builder /venv /venv
ENV PATH /venv/bin:$PATH

# configure python env
ENV PYTHONPATH $APP_HOME
ENV PYTHONUNBUFFERED 1

# make entrypoint script executable 
RUN chmod +x  $APP_HOME/entrypoint.sh

# chown all the files to the app user
RUN chown -R $UNAME:$UNAME $HOME

# switch to app user
USER $UNAME
