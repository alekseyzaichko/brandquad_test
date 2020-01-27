FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh

ADD wait-for-it.sh /
RUN chmod +x /wait-for-it.sh

COPY . .

ENTRYPOINT ["/entrypoint.sh"]