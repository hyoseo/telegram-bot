FROM        python:3.8-buster
MAINTAINER 	hyoseo87@gmail.com
ENV         TZ=Asia/Seoul
RUN		    ln -snf /usr/share/zoneinfo/\$TZ /etc/localtime && \
            echo \$TZ > /etc/timezone
COPY        . /app
RUN         pip install -r /app/requirements.txt
WORKDIR     /app
ENTRYPOINT  ["python", "main.py"]