FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
RUN pip3 install flask
RUN echo "SSS{test-flag}" > /flag.txt
RUN useradd ctf && mkdir uploads
COPY . /app
RUN chown -R root:ctf /app && chmod -R 550 /app
RUN chmod 770 health.py && chmod -R 770 /app/uploads
USER ctf
CMD ["python3", "app.py"]