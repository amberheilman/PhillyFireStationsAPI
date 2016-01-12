FROM python
MAINTAINER Amber Heilman
RUN python app.py
ENV PGSQL_URI=postgresql://fire_read@localhost:5432/philly_fire
EXPOSE 8000
