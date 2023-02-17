FROM python:latest

COPY index.html .
COPY index.py .
COPY ["/Pyscript Website", "/Pyscript Website/"]

CMD python -m http.server 5500