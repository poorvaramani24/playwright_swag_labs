FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN playwright install

CMD ["pytest", "-n", "auto"]