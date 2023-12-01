FROM python:3.10.12-alpine
WORKDIR /simple_solutions_stripe
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=simple_solutions_stripe.settings_prod
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
# copy project
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh