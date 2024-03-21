create database SocieteT
GO
use SocieteT
GO

create table depot
(idlocation int identity(1,1) primary key,
unelocation varchar(20),
capacite float)

create table Produits
(idproduits int identity(1,1) primary key, 
nomproduits varchar(20),
prixunitaire float)
create table commande
(idcommande int identity(1,1) primary key,
datecommande Date,
idlocation int)

create table details_commande
(idcommande int not null , 
idproduits int not null , 
qtecommande float)

alter table details_commande add constraint fk_produit foreign key (idproduits) references  Produits(idproduits)
alter table details_commande add constraint fk_commande foreign key (idcommande) references  commande(idcommande)
alter table details_commande add constraint pk_detailcommande primary key (idcommande,idproduits) 
alter table commande add constraint fk_location foreign key (idlocation) references depot(idlocation)

create table Inventaire
(idproduits int not null , idlocation int not null,Qte float)

alter table Inventaire add constraint fk_inventaireprod foreign key (idproduits) references  Produits(idproduits)
alter table Inventaire add constraint fk_inventaireloc foreign key (idlocation) references  depot(idlocation)
alter table Inventaire add constraint pk_inventaire primary key (idproduits,idlocation) 



insert into Produits values ('TV 65 pouces', 800),
							('TV 50 pouces', 400),
							('TV 42 pouces', 300)