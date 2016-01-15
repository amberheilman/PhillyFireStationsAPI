FROM python
MAINTAINER Amber Heilman
COPY dist
RUN pip install dist/emswatch*.whl
ENV PGSQL_URI=postgresql://fire_read@localhost:5432/philly_fire
EXPOSE 8000
ENTRYPOINT python app.py
