FROM python:3.9
RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
WORKDIR /usr/app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]