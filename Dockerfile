FROM python:latest

COPY index.html .
COPY index.py .
COPY requirements/web-app.txt .
COPY ["/ML","/ML/"]
COPY ["/ETL_pipeline", "/ETL_pipeline/"]
COPY ["/Pyscript_Website", "/Pyscript_Website/"]
RUN pip install -r web-app.txt

CMD python -m http.server 5500