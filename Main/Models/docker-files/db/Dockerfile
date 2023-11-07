FROM mysql:8.0.33

ENV MYSQL_ROOT_PASSWORD="admin"
ENV MYSQL_DATABASE="crypto_analysis"

# Copy the SQL script to the image
ADD db_backup.sql docker-entrypoint-initdb.d/db_backup.sql
