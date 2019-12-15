import os
import sys

import psycopg2 as dbapi2

url= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"


INIT_STATEMENTS = [
   '''
    create table IF NOT EXISTS PERSONNEL (
        ID SERIAL PRIMARY KEY,
        Name varchar(50) NOT NULL,
        Surname varchar(50) NOT NULL,
        Department varchar(50) NOT NULL,
        Professional_Title varchar(50) NOT NULL,
        Phone_Number varchar(13) NOT NULL,
        Email_Address varchar(50) NOT NULL
        ); 
   
	create table IF NOT EXISTS DEPARTMENTS (
		Department_Name varchar(100) PRIMARY KEY,
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
		Department varchar(100) NOT NULL,
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
        Attendance BOOLEAN,
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

# ALTER TABLE PLACES
    # ADD CONSTRAINT fk_places_type
        # FOREIGN KEY (Type) REFERENCES TECH(Name);
        
# ALTER TABLE PLACES
    # ADD CONSTRAINT fk_places_department
        # FOREIGN KEY (Department) REFERENCES DEPARTMENTS(Department_Name);
        
# ALTER TABLE MEETINGS
    # ADD CONSTRAINT fk_meetings_place_id
        # FOREIGN KEY (Place_ID) REFERENCES PLACES(ID);
        
# ALTER TABLE PERSONNEL
    # ADD CONSTRAINT fk_personnel_department     
        # FOREIGN KEY (Department) REFERENCES DEPARTMENTS(Department_Name);
        
# ALTER TABLE PARTICIPANTS  
    # ADD CONSTRAINT fk_participants_meeting_id
        # FOREIGN KEY (Meeting_ID) REFERENCES MEETINGS(ID);
        
# ALTER TABLE PARTICIPANTS  
    # ADD CONSTRAINT fk_participants_person_id
        # FOREIGN KEY (Person_ID) REFERENCES PERSONNEL(ID);

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
#    url = os.getenv("DATABASE_URL")
#    if url is None:
#        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
#        sys.exit(1)
    initialize(url)
    add_fk_to_personnel(url)
    
