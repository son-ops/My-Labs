FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip3 install flask
RUN chmod +x entrypoint.sh
CMD ["/app/entrypoint.sh"]