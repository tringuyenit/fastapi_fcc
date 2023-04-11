FROM python:3.9.7

WORKDIR usr/src/app

RUN apt-get update && apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# #CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
# #CMD ["uvicorn app.main:app --host 0.0.0.0 --port 8001"]

CMD ["/usr/bin/supervisord"]
