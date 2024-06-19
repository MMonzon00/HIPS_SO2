#!/bin/bash

# Variables
DB_NAME="HIPS_LOGS"
DB_USER="admin"
DB_PASSWORD="admin123"
PG_VERSION="13"

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to the postgres user and create a database and user
sudo -i -u postgres psql <<EOF
-- Create the database
CREATE DATABASE $DB_NAME;

-- Create the user with a password
CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- (Optional) Set the default encoding, locale, and collation
ALTER DATABASE $DB_NAME SET client_encoding TO 'utf8';
ALTER DATABASE $DB_NAME SET lc_collate TO 'en_US.UTF-8';
ALTER DATABASE $DB_NAME SET lc_ctype TO 'en_US.UTF-8';
ALTER DATABASE $DB_NAME SET default_text_search_config TO 'pg_catalog.english';
EOF

# Print success message
echo "PostgreSQL database setup completed."
echo "Database: $DB_NAME"
echo "Username: $DB_USER"
echo "Password: $DB_PASSWORD"
