FROM python:3.10

 

RUN mkdir /code

 

WORKDIR /code

 

COPY requirements.txt .
RUN pip install --upgrade pip
RUN apt-get update

 

RUN pip install -r requirements.txt

 

COPY . .

 

RUN python -m fetch_latest_match_id

 

RUN python -m match_output

 

RUN python -m pred
