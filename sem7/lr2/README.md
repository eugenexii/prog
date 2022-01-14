from python:latest
copy index.html /home/app/
expose 80
CMD python -m http.server 80