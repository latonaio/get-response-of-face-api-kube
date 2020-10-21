FROM l4t:latest

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
RUN pip3 install -r ./requirements.txt

CMD ["sh", "entrypoint.sh"]


