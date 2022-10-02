FROM python:3.9
RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
WORKDIR /usr/app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV QUART_APP=application:app
ENV QUART_ENV=development
#CMD [ "python3", "-m" , "quart", "run", "--host=0.0.0.0"]
CMD [ "hypercorn", "application:app", "--bind" , "0.0.0.0:5000", "--reload"]

#CMD ["sleep", "infinity"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]