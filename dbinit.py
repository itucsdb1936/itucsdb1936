import os
import sys

import psycopg2 as dbapi2

#url= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"


INIT_STATEMENTS = [
   '''
	create table IF NOT EXISTS DEPARTMENTS (
		Department_Name varchar(100) PRIMARY KEY,
		Manager varchar(100) NOT NULL,
		Location varchar(50) NOT NULL,
		Capacity INT NOT NULL,
		Website varchar(100)
        );
	
	create table IF NOT EXISTS ROOM_TYPES (
		Type VARCHAR(100) PRIMARY KEY,
		Projector VARCHAR(100),
		Presentation_Computer VARCHAR(100),
		WhiteBoard VARCHAR(50)
        );
	
	create table IF NOT EXISTS PLACES (
		ID SERIAL PRIMARY KEY,
		Type varchar(100) NOT NULL,
		Department varchar(100) NOT NULL,
		Location varchar(100) NOT NULL,
		Capacity INT NOT NULL,
        );
        
   create table IF NOT EXISTS MEETINGS (
        ID SERIAL PRIMARY KEY,
        Place_ID int NOT NULL,
        Date date NOT NULL,
        Time time NOT NULL,
        Topic varchar(500)NOT NULL,
        );	
	
   create table IF NOT EXISTS PERSONNEL (
        ID SERIAL PRIMARY KEY,
        Name varchar(50) NOT NULL,
        Surname varchar(50) NOT NULL,
        Department varchar(50) NOT NULL,
	Professional_Title varchar(50) NOT NULL,
        Phone_Number varchar(13) NOT NULL,
	Email_Address varchar(50) NOT NULL,
        );

   create table IF NOT EXISTS PARTICIPANTS (
	Meeting_ID INT NOT NULL,
	Person_ID INT NOT NULL,
	Role varchar(50) NOT NULL,
	Attendance BOOLEAN,
	Performance varchar(500),
	PRIMARY KEY (Meeting_ID,Person_ID),
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

#FOREIGN KEY (Type) REFERENCES ROOM_TYPES(Type),
#FOREIGN KEY (Department) REFERENCES DEPARTMENTS(Department_Name)
#FOREIGN KEY (Place_ID) REFERENCES PLACES(ID)
#FOREIGN KEY (Department) REFERENCES DEPARTMENTS(Department_Name)
#FOREIGN KEY (Meeting_ID) REFERENCES MEETINGS(ID),
#FOREIGN KEY (Person_ID) REFERENCES PERSONNEL(ID)


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
