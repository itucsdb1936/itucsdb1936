Parts Implemented by Huveyscan Kamar
================================
			  
	I hope this guide answers all your questions and can help you to implement a meeting module like this one. Good luck!

General Logic
~~~~~~~~~~~~~
First, I designed the page according to the table. And placed the buttons according to table's functions.
Second, I defined the page and also defined an app route to it. 
Third, I designed pages to be used for the functions I am going to implement such as create, read, update and remove.
Fourth, I defined function pages and also defined app routes to them. 
Fifth, I implemented needed functions to be used in the page such as create, read, update and remove.
Sixth, I placed the functions to the buttons and icons on the related page.

As an example, all functions of Personnel Table are added. The other table's functions are implemented with almost the same logic.

Personnel Table
~~~~~~~~~~~~~~~


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
------------------------------
		.. figure:: AppRoutesForPersonnel.png
			  :scale: 80 %
			  :alt: App Routes for Personnel Table 
			  :align: center

			  App Routes for Personnel Table 



Add Personnel Function
----------------------

		.. figure:: AddPersonnelFunction.png
			  :scale: 50 %
			  :alt: Add Personnel Function
			  :align: center

			  Add Personnel Function 

Update Personnel Function
-------------------------
			 
		.. figure:: UpdatePersonnelFunction.png
			  :scale: 50 %
			  :alt: Update Personnel Function
			  :align: center

			  Update Personnel Function
			 
Delete Personnel Function
-------------------------
			 
		.. figure:: RemovePersonnelFunction.png
			  :scale: 100 %
			  :alt: Delete Personnel Function
			  :align: center

			  Delete Personnel Function

Delete Multiple Personnel Function
----------------------------------
			 
		.. figure:: RemoveMultiplePersonnelFunction.png
			  :scale: 100 %
			  :alt: Delete Multiple Personnel Function
			  :align: center

			  Delete Multiple Personnel Function

Places Table
~~~~~~~~~~~~

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
------------------------

		.. figure:: AppRoutesForPlaces.png
			  :scale: 80 %
			  :alt: App Routes for Places Table 
			  :align: center

			  App Routes for Places Table 

Participants Table
~~~~~~~~~~~~~~~~~~

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
---------------------------------
		.. figure:: AppRoutesForParticipants.png
			  :scale: 90 %
			  :alt: App Routes for Participants Table 
			  :align: center

			  App Routes for Participants Table 
			  
