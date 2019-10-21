import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS MEETINGS (topic varchar(64), room int)",
    "INSERT INTO MEETINGS VALUES ('flask project', '216')",
    "INSERT INTO MEETINGS VALUES ('coffee machine', '104')",
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
#    if url is None:
#        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
#        sys.exit(1)
    initialize(url)
