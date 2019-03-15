CREATE TABLE cart ( id varchar PRIMARY KEY NOT NULL );
CREATE TABLE item ( external_id varchar, name varchar, value integer, cart_id varchar, PRIMARY KEY (external_id, cart_id) );

