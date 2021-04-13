# syntax = docker/dockerfile:1.0.0-experimental
FROM latonaio/l4t:latest

# Definition of a Device & Service
ENV POSITION=Runtime \
    SERVICE=get-response-of-face-api \
    AION_HOME=/var/lib/aion

# Setup Directoties
RUN mkdir -p /${AION_HOME}/$POSITION/$SERVICE

WORKDIR /${AION_HOME}/$POSITION/$SERVICE


ADD . .

# Install dependencies
RUN pip3 install --upgrade pip
RUN --mount=type=secret,id=ssh,target=/root/.ssh/id_rsa ssh-keyscan -t rsa bitbucket.org >> /root/.ssh/known_hosts \
  && pip3 install -U git+ssh://git@bitbucket.org/latonaio/aion-related-python-library.git
#RUN python3 setup.py install
RUN pip3 install -r ./requirements.txt

CMD ["sh", "entrypoint.sh"]


