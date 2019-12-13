import os
import sys

import psycopg2 as dbapi2

#url= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"


INIT_STATEMENTS = [
   '''
   create table IF NOT EXISTS MEETINGS (
        ID SERIAL PRIMARY KEY,
        PlaceID int NOT NULL,
        StatusID int NOT NULL,
        DATE date NOT NULL,
        TIME time NOT NULL,
        Duration time,
        Topic varchar(500)NOT NULL,
        RESULT varchar(1500)
        );
   create table IF NOT EXISTS TECH (
        Name VARCHAR(100) PRIMARY KEY,
        Projector VARCHAR(100),
        Speaker VARCHAR(100),
        Computer VARCHAR(100),
        DigitalWhiteboard VARCHAR(100),
        Manuals BYTEA
        );
   create table IF NOT EXISTS COMMENTS (
        CommentID SERIAL PRIMARY KEY,
        Name VARCHAR(100) NOT NULL,
        Comment TEXT,
        Score INT NOT NULL
            check(Score >= 1 and Score <= 5)
        );
   '''
   ]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
