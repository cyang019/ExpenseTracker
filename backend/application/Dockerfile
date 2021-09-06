FROM python:latest
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app
COPY models.py models.py
ENTRYPOINT ["python3"]
CMD ["api.py"]
