FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -m hp && mkdir /data && chown hp /data
COPY *.py ./
USER hp
EXPOSE 2121 2222 2323 33306 33389 8080 8081
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request as u; u.urlopen('http://127.0.0.1:8081/healthz', timeout=2)"
ENTRYPOINT ["python", "main.py", "--data-dir", "/data", "--dashboard-host", "0.0.0.0"]
