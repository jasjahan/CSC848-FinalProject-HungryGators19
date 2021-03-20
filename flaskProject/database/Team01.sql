-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema HungryGators-19
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `HungryGators-19` DEFAULT CHARACTER SET utf8 ;
USE `HungryGators-19` ;

-- -----------------------------------------------------
-- Table `HungryGators-19`.`takeout_order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`takeout_order` (
  `idtakeout_order` TINYINT NOT NULL AUTO_INCREMENT,
  `item` VARCHAR(45) NULL,
  `price` DECIMAL NULL,
  PRIMARY KEY (`idtakeout_order`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`receipt`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`receipt` (
  `idreceipt` TINYINT NOT NULL AUTO_INCREMENT,
  `item_description` VARCHAR(45) NULL,
  `item_price` VARCHAR(45) NULL,
  `item_name` VARCHAR(45) NULL,
  PRIMARY KEY (`idreceipt`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`sfsu_customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`sfsu_customer` (
  `idsfsu_customer` TINYINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `address` VARCHAR(45) NULL,
  `zip_code` VARCHAR(45) NULL,
  PRIMARY KEY (`idsfsu_customer`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`review`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`review` (
  `idreview` TINYINT NOT NULL AUTO_INCREMENT,
  `review` VARCHAR(500) NULL,
  `sfsu_customer` TINYINT NOT NULL,
  PRIMARY KEY (`idreview`, `sfsu_customer`),
  INDEX `Customer_FK_idx` (`sfsu_customer` ASC) VISIBLE,
  CONSTRAINT `Customer_FK`
    FOREIGN KEY (`sfsu_customer`)
    REFERENCES `HungryGators-19`.`sfsu_customer` (`idsfsu_customer`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`delivery_employee`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`delivery_employee` (
  `iddelivery_employee` TINYINT NOT NULL,
  `target_address` VARCHAR(45) NULL,
  `delivery_time` VARCHAR(45) NULL,
  `pickup_address` VARCHAR(45) NULL,
  `pickup_time` VARCHAR(45) NULL,
  PRIMARY KEY (`iddelivery_employee`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`person` (
  `idperson` TINYINT NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(45) NULL,
  `age` VARCHAR(45) NULL,
  `sfsu_customer_id` TINYINT NOT NULL,
  `delivery_employee` TINYINT NOT NULL,
  PRIMARY KEY (`idperson`, `delivery_employee`, `sfsu_customer_id`),
  INDEX `Customer_Person_FK_idx` (`sfsu_customer_id` ASC) VISIBLE,
  INDEX `Delivery_Person_FK_idx` (`delivery_employee` ASC) VISIBLE,
  CONSTRAINT `Customer_Person_FK`
    FOREIGN KEY (`sfsu_customer_id`)
    REFERENCES `HungryGators-19`.`sfsu_customer` (`idsfsu_customer`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Delivery_Person_FK`
    FOREIGN KEY (`delivery_employee`)
    REFERENCES `HungryGators-19`.`delivery_employee` (`iddelivery_employee`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`restaurant`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`restaurant` (
  `idrestaurant` TINYINT NOT NULL AUTO_INCREMENT,
  `address` VARCHAR(45) NULL,
  `phone_number` VARCHAR(45) NULL,
  `zip_code` VARCHAR(45) NULL,
  PRIMARY KEY (`idrestaurant`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`user_reg_record`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`user_reg_record` (
  `iduser_reg_record` TINYINT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  PRIMARY KEY (`iduser_reg_record`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`delivery_driver_record`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`delivery_driver_record` (
  `iddelivery_driver_record` TINYINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `vehicle` VARCHAR(45) NULL,
  PRIMARY KEY (`iddelivery_driver_record`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`customer_orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`customer_orders` (
  `idcustomer_orders` TINYINT NOT NULL AUTO_INCREMENT,
  `customer` TINYINT NOT NULL,
  `takeout_order` TINYINT NOT NULL,
  PRIMARY KEY (`idcustomer_orders`, `customer`, `takeout_order`),
  INDEX `sfsu_customer_idx` (`customer` ASC) VISIBLE,
  INDEX `takeout_order_idx` (`takeout_order` ASC) VISIBLE,
  CONSTRAINT `Customer_FK_PK`
    FOREIGN KEY (`customer`)
    REFERENCES `HungryGators-19`.`sfsu_customer` (`idsfsu_customer`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Takeout_Order_FK_PK`
    FOREIGN KEY (`takeout_order`)
    REFERENCES `HungryGators-19`.`takeout_order` (`idtakeout_order`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`customer_receipts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`customer_receipts` (
  `idcustomer_receipts` TINYINT NOT NULL AUTO_INCREMENT,
  `customer` TINYINT NOT NULL,
  `receipt` TINYINT NOT NULL,
  PRIMARY KEY (`idcustomer_receipts`, `customer`, `receipt`),
  INDEX `Receipt_FK_idx` (`receipt` ASC) VISIBLE,
  INDEX `Customer_FK_idx` (`customer` ASC) VISIBLE,
  CONSTRAINT `Customer_Customer_Receipts_FK`
    FOREIGN KEY (`customer`)
    REFERENCES `HungryGators-19`.`sfsu_customer` (`idsfsu_customer`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Customer_Receipt_FK`
    FOREIGN KEY (`receipt`)
    REFERENCES `HungryGators-19`.`receipt` (`idreceipt`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`records`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`records` (
  `idrecords` TINYINT NOT NULL AUTO_INCREMENT,
  `restaurant` TINYINT NOT NULL,
  `delivery_driver_record` TINYINT NOT NULL,
  `user_reg_record` TINYINT NOT NULL,
  PRIMARY KEY (`idrecords`, `restaurant`, `delivery_driver_record`, `user_reg_record`),
  INDEX `Delivery_Driver_Record_FK_idx` (`delivery_driver_record` ASC) VISIBLE,
  INDEX `User_Reg_Record_FK_idx` (`user_reg_record` ASC) VISIBLE,
  INDEX `Restaurant_FK_idx` (`restaurant` ASC) VISIBLE,
  CONSTRAINT `Delivery_Driver_Record_FK`
    FOREIGN KEY (`delivery_driver_record`)
    REFERENCES `HungryGators-19`.`delivery_driver_record` (`iddelivery_driver_record`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `User_Reg_Record_FK`
    FOREIGN KEY (`user_reg_record`)
    REFERENCES `HungryGators-19`.`user_reg_record` (`iduser_reg_record`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Restaurant_FK`
    FOREIGN KEY (`restaurant`)
    REFERENCES `HungryGators-19`.`restaurant` (`idrestaurant`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `HungryGators-19`.`restaurant_person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HungryGators-19`.`restaurant_person` (
  `idrestaurant_person` TINYINT NOT NULL,
  `idrestaurant` TINYINT NOT NULL,
  `idperson` TINYINT NOT NULL,
  PRIMARY KEY (`idrestaurant_person`, `idrestaurant`, `idperson`),
  INDEX `Restaurant_FK_idx` (`idrestaurant` ASC) VISIBLE,
  INDEX `Person_FK_PK_idx` (`idperson` ASC) VISIBLE,
  CONSTRAINT `Restaurant_FK_PK`
    FOREIGN KEY (`idrestaurant`)
    REFERENCES `HungryGators-19`.`restaurant` (`idrestaurant`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Person_FK_PK`
    FOREIGN KEY (`idperson`)
    REFERENCES `HungryGators-19`.`person` (`idperson`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
