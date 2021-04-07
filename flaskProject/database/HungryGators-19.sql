CREATE SCHEMA IF NOT EXISTS `HungryGators-19` DEFAULT CHARACTER SET utf8 ;
USE `HungryGators-19` ;
CREATE TABLE restaurant (
  id tinyint(4) NOT NULL AUTO_INCREMENT,
  name varchar(45) NOT NULL,
  address varchar(45) DEFAULT NULL,
  phone_number varchar(45) DEFAULT NULL,
  zip_code varchar(45) DEFAULT NULL,
  image varchar(100) NOT NULL,
  cuisine varchar(45) NOT NULL,
  PRIMARY KEY (id)
);


CREATE TABLE menu (
  id tinyint(4) NOT NULL AUTO_INCREMENT,
  name varchar(45) DEFAULT NULL,
  price float NOT NULL,
  quantity int(11) DEFAULT NULL,
  restaurant_id tinyint(4) NOT NULL,
  PRIMARY KEY (id),
  KEY id_idx (restaurant_id)
);