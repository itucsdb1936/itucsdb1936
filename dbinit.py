import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
   '''
        create table IF NOT EXISTS PERSONNEL (
        ID SERIAL PRIMARY KEY,
        Name varchar(50) NOT NULL,
        Surname varchar(50) NOT NULL,
        Department varchar(50) NOT NULL,
        Professional_Title varchar(50) NOT NULL,
        Phone_Number varchar(20) NOT NULL,
        Email_Address varchar(50) NOT NULL,
	Pictures BYTEA
        ); 
   
	create table IF NOT EXISTS DEPARTMENTS (
		Department_Name varchar(50) PRIMARY KEY,
		Manager_ID INT,
		Location varchar(50) NOT NULL,
		Capacity INT NOT NULL,
		Website varchar(100),
        FOREIGN KEY (Manager_ID) REFERENCES PERSONNEL(ID)
        );
        
	create table IF NOT EXISTS ROOM_TYPES (
		Type VARCHAR(100) PRIMARY KEY,
		Projector VARCHAR(100),
		Presentation_Computer VARCHAR(100),
        WhiteBoard VARCHAR(50)
        );
	
    create table IF NOT EXISTS TECH (
        Name VARCHAR(100) PRIMARY KEY,
        Projector VARCHAR(100),
        Speaker VARCHAR(100),
        Computer VARCHAR(100),
        DigitalWhiteboard VARCHAR(100),
        Manuals BYTEA
        );
    
	create table IF NOT EXISTS PLACES (
		ID SERIAL PRIMARY KEY,
		Type varchar(100) NOT NULL,
		Department varchar(50) NOT NULL,
		Location varchar(100) NOT NULL,
		Capacity INT NOT NULL,
        FOREIGN KEY (Type) REFERENCES TECH(Name),
        FOREIGN KEY (Department) REFERENCES DEPARTMENTS(Department_Name)
        );
        
   create table IF NOT EXISTS MEETINGS (
        ID SERIAL PRIMARY KEY,
        Place_ID INT,
        Date date NOT NULL,
        Time time NOT NULL,
        Topic varchar(500) NOT NULL,
        FOREIGN KEY (Place_ID) REFERENCES PLACES(ID)
        );	
	
   
   create table IF NOT EXISTS PARTICIPANTS (
        Meeting_ID INT NOT NULL,
        Person_ID INT NOT NULL,
        Role varchar(50),
        Attendance varchar(50),
        Performance varchar(500),
        PRIMARY KEY (Meeting_ID,Person_ID),
        FOREIGN KEY (Meeting_ID) REFERENCES MEETINGS(ID),
        FOREIGN KEY (Person_ID) REFERENCES PERSONNEL(ID)
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

def add_fk_to_personnel(url):
    alter = "ALTER TABLE PERSONNEL ADD CONSTRAINT fk_personnel_department FOREIGN KEY (Department) REFERENCES DEPARTMENTS(Department_Name)"
    connection = dbapi2.connect(url)
    try:
        cursor = connection.cursor()
        cursor.execute(alter)
        connection.commit()
        cursor.close()
    except dbapi2.DatabaseError:
        connection.rollback()
    finally:
        connection.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
       print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
       sys.exit(1)
    initialize(url)
    add_fk_to_personnel(url)
    
