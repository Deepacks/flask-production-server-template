FROM deepacks/python-enhanced:3.9.9-alpine3.15-amd64

WORKDIR /usr/src/app

COPY . .

RUN source ./environment/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

CMD [ "gunicorn", "main:app", "--access-logfile", "'-'" ]
