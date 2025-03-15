FROM python:3.10

COPY ./rss_retriever/rss_parser.py rss_parser.py
COPY ./rss_retriever/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


CMD ["python3", "-u","/rss_parser.py"]
