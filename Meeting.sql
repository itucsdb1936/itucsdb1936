create table Meeting (
ID int NOT NULL,
PlaceID int NOT NULL,
StatusID int NOT NULL,
DATE date NOT NULL,
TIME time NOT NULL,
Duration time,
Topic varchar(500)NOT NULL,
RESULT varchar(1500),
PRIMARY key (ID)
);