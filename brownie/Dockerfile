FROM python:3.10

COPY ./brownie/main.py main.py
COPY ./brownie/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7000
CMD ["python3", "-u","/main.py"]
