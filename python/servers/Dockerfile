FROM python:2.7-alpine

COPY . /app
WORKDIR /app

RUN ls
RUN pip install -r requirements.txt

CMD python wiki.py TSWiki w 80 /var/www/pages /var/www/service_pages /var/www/assets 
