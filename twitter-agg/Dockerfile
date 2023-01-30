FROM python:3.9
RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
WORKDIR /usr/app
COPY . ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ARG BEARER=default_bearer
ENV BEARER=${BEARER}
ENV QUART_APP=application:app
ENV QUART_ENV=development
CMD [ "hypercorn", "application:app", "--bind" , "0.0.0.0:5000", "--reload"]