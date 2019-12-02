import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
   '''create table IF NOT EXISTS MEETINGS (
        ID SERIAL PRIMARY KEY,
        PlaceID int NOT NULL,
        StatusID int NOT NULL,
        DATE date NOT NULL,
        TIME time NOT NULL,
        Duration time,
        Topic varchar(500)NOT NULL,
        RESULT varchar(1500)
        );''']


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
