CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `user_type` int(2) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

CREATE TABLE `restaurant` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone_number` varchar(45) DEFAULT NULL,
  `zip_code` varchar(45) DEFAULT NULL,
  `image` varchar(100) NOT NULL,
  `cuisine` varchar(45) NOT NULL,
  `description` varchar(300) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `price_tag` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;

CREATE TABLE `menu` (
  `id` tinyint(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `price` float NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `restaurant_id` tinyint(4) NOT NULL,
  `active` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `id_idx` (`restaurant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;

CREATE TABLE `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phone_number` varchar(45) DEFAULT NULL,
  `mode` varchar(45) DEFAULT NULL,
  `total` float DEFAULT NULL,
  `items` json DEFAULT NULL,
  `active` tinyint(4) DEFAULT NULL,
  `driver_id` int(11) DEFAULT NULL,
  `restaurant_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;