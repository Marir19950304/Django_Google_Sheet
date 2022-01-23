CREATE DATABASE jzprop;
CREATE USER jzpropuser WITH PASSWORD 'jzpropuser1';
ALTER ROLE jzpropuser SET client_encoding TO 'utf8';
ALTER ROLE jzpropuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE jzpropuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE jzprop TO jzpropuser;



