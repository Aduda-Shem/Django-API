FROM python:3.8

WORKDIR /app/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
# RUN apt-get update && apt-get upgrade

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh /app/backend/
RUN sed -i 's/\r$//g' /app/backend/entrypoint.sh
RUN chmod +x /app/backend/entrypoint.sh

# Copy the rest of the application code
COPY . /app/backend/

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

ENTRYPOINT ["/app/backend/entrypoint.sh"]