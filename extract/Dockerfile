FROM python:3.10-slim

# install PostgreSQL command-line tools
RUN apt-get update && apt-get install -y postgresql-client cron

# copy the ETL script
# COPY start.sh /app/start.sh
COPY to_lake.py .

# WORKDIR /app

# RUN echo "0 3 * * * python /app/to_lake.py" | crontab -

# Set the default command to run the etl script
CMD [ "python", "to_lake.py" ]