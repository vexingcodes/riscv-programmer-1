FROM debian:9.5 as base
RUN apt-get update \
 && apt-get install --yes --no-install-recommends apt-transport-https ca-certificates curl gnupg \
 && curl -sL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add - \
 && curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
 && echo 'deb https://deb.nodesource.com/node_8.x stretch main' > /etc/apt/sources.list.d/nodesource.list \
 && echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list \
 && apt-get update \
 && apt-get install --yes --no-install-recommends build-essential python3 python3-pip python3-dev \
 && apt-get install --yes yarn \
 && pip3 install pipenv
ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 PIPENV_PIPFILE=/code/Pipfile
WORKDIR /code

FROM base as production

# Copy the code.
COPY Pipfile Pipfile.lock package.json yarn.lock gulpfile.js ./
COPY src ./src

# Install python/js packages and generate css/js sources.
RUN pipenv install --system --deploy \
 && yarn install \
 && ./node_modules/.bin/gulp sass js

# Run the server as a non-root user on port 5000.
RUN groupadd user && useradd -r -g user user && chown -R user:user /code
USER user
WORKDIR /code/src
EXPOSE 5000
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "server:APPLICATION"]

FROM base as development

RUN apt-get update \
 && apt-get install --yes --no-install-recommends supervisor

#ARG DEV_UID
#ARG DEV_GID
#RUN test -n "$DEV_UID" && test -n "$DEV_GID"

VOLUME /code
EXPOSE 5000
EXPOSE 3000
EXPOSE 3001
COPY dev.sh dev.supervisor.conf /
CMD ["/dev.sh"]
