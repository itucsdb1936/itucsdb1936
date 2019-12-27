Parts Implemented by Huveyscan Kamar
================================
General Logic
~~~~~~~~~~~~~
First, I designed the page according to the table. And placed the buttons according to table's functions.
Second, I defined the page and also defined an app route to it. 
Third, I designed pages to be used for the functions I am going to implement such as create, read, update and remove.
Fourth, I defined function pages and also defined app routes to them. 
Fifth, I implemented needed functions to be used in the page such as create, read, update and remove.
Sixth, I placed the functions to the buttons and icons on the related page.

Personnel Table
--------------

*Table of this database: 
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
			  
I've implemented create, read, update and remove functions for this table.

App Routes for Personnel Table 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		.. figure:: AppRoutesForPersonnel.png
			  :scale: 80 %
			  :alt: App Routes for Personnel Table 
			  :align: center

			  App Routes for Personnel Table 



Add Personnel Function
~~~~~~~~~~~~~~~~~~~~~~~

		.. figure:: AddPersonnelFunction.png
			  :scale: 50 %
			  :alt: Add Personnel Function
			  :align: center

			  Add Personnel Function 

Update Personnel
~~~~~~~~~~~~~~~~
			  
Delete Personnel
~~~~~~~~~~~~~~~~

Places Table
--------------

*Table of this database: 
	create table IF NOT EXISTS PLACES (
		ID SERIAL PRIMARY KEY,
		Type varchar(100) NOT NULL,
		Department varchar(50) NOT NULL,
		Location varchar(100) NOT NULL,
		Capacity INT NOT NULL,
        FOREIGN KEY (Type) REFERENCES TECH(Name),
        FOREIGN KEY (Department) REFERENCES DEPARTMENTS(Department_Name)
        );

App Routes for Places Table 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		.. figure:: AppRoutesForPlaces.png
			  :scale: 80 %
			  :alt: App Routes for Places Table 
			  :align: center

			  App Routes for Places Table 

Add Places
~~~~~~~~~~~~~

Update Places
~~~~~~~~~~~~~~~~
			  
Delete Places
~~~~~~~~~~~~~~~~

Participants Table
--------------

*Table of this database: 
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

App Routes for Participants Table 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		.. figure:: AppRoutesForParticipants.png
			  :scale: 90 %
			  :alt: App Routes for Participants Table 
			  :align: center

			  App Routes for Participants Table 


Add Participants
~~~~~~~~~~~~~

Update Participants
~~~~~~~~~~~~~~~~
			  
Delete Participants
~~~~~~~~~~~~~~~~

	.. figure:: .png
			  :scale: 100 %
			  :alt: 
			  :align: center

			  Text