FROM python:latest

WORKDIR /project/data

COPY requirements.txt .
#copy project dependcies
RUN "pip install -r requirements.txt"

#copy projects files
COPY . .

CMD ["uvicorn", "main:app"]