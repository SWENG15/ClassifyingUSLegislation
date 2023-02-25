FROM python:latest

COPY index.html .
COPY index.py .
COPY ["/Pyscript_Website", "/Pyscript_Website/"]

CMD python -m http.server 5500