FROM python:3.6-alpine AS compiler-enabled
RUN apk add --no-cache gcc musl-dev linux-headers

FROM compiler-enabled AS buildenv
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

FROM buildenv as API
WORKDIR /app
ENV DEBUG yes
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM buildenv as WSOCKET
WORKDIR /app
ADD tornado_broadcaster.py .
CMD ["python", "tornado_broadcaster.py"]

