FROM python:3

WORKDIR /usr/local/src

RUN groupadd -r gradgyde &&\
    useradd --no-log-init -r -g gradgyde gradgyde &&\
    mkdir -p /run/wsgi &&\
    chown gradgyde:gradgyde /usr/local/src /run/wsgi

VOLUME /run/wsgi

COPY --chown=gradgyde:gradgyde requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uwsgi

COPY --chown=gradgyde:gradgyde . .

USER gradgyde

ENTRYPOINT ["uwsgi", "--ini", "wsgi.ini"]