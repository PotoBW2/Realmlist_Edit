CREATE TABLE ip (
	id_ip               integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
	primero             integer(3) DEFAULT 192 NOT NULL, 
	segundo             integer(3) DEFAULT 168 NOT NULL, 
	tercero             integer(3) DEFAULT 1 NOT NULL, 
	cuarto              integer(3) DEFAULT 0 NOT NULL, 
	Servidorid_servidor integer(2) NOT NULL,  
	FOREIGN KEY(Servidorid_servidor) REFERENCES Servidor(id_servidor));
CREATE TABLE Servidor (
  id_servidor     integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  nombre_servidor varchar(20) NOT NULL UNIQUE
	);
CREATE TABLE url (
  id_url              integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
  direccion           varchar(30) NOT NULL UNIQUE, 
  Servidorid_servidor integer(2) NOT NULL,
  FOREIGN KEY(Servidorid_servidor) REFERENCES Servidor(id_servidor));
CREATE UNIQUE INDEX ip_id_ip 
	ON ip (id_ip);
CREATE UNIQUE INDEX Servidor_id_servidor 
	ON Servidor (id_servidor);
CREATE UNIQUE INDEX url_id_url 
	ON url (id_url);





