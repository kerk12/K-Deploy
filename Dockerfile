FROM python:3

COPY . /usr/src/app/
WORKDIR /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]