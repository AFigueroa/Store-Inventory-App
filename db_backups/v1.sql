# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.33)
# Database: itemsdb
# Generation Time: 2014-09-02 04:33:39 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table items
# ------------------------------------------------------------

DROP TABLE IF EXISTS `items`;

CREATE TABLE `items` (
  `itemId` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) NOT NULL,
  `itemName` varchar(50) NOT NULL DEFAULT '',
  `itemDescription` text NOT NULL,
  `itemWidth` int(11) DEFAULT NULL,
  `itemLength` int(11) DEFAULT NULL,
  `itemHeight` int(11) DEFAULT NULL,
  `itemWeight` int(11) DEFAULT NULL,
  `active` int(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`itemId`),
  UNIQUE KEY `itemName` (`itemName`),
  KEY `userid` (`userid`),
  KEY `active` (`active`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;

INSERT INTO `items` (`itemId`, `userid`, `itemName`, `itemDescription`, `itemWidth`, `itemLength`, `itemHeight`, `itemWeight`, `active`)
VALUES
	(1,1,'Tables','Tan, Darkbark',4,3,2,20,1),
	(2,1,'new',' Item description here',1,1,1,1,0),
	(3,1,'newe\'',' Item description here',1,1,1,1,0);

/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table pictures
# ------------------------------------------------------------

DROP TABLE IF EXISTS `pictures`;

CREATE TABLE `pictures` (
  `pictureId` int(11) NOT NULL AUTO_INCREMENT,
  `itemId` int(11) NOT NULL,
  `pictureUrl` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`pictureId`),
  UNIQUE KEY `pictureUrl` (`pictureUrl`),
  KEY `itemid` (`itemId`),
  CONSTRAINT `pictures_ibfk_1` FOREIGN KEY (`itemid`) REFERENCES `items` (`itemid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `pictures` WRITE;
/*!40000 ALTER TABLE `pictures` DISABLE KEYS */;

INSERT INTO `pictures` (`pictureId`, `itemId`, `pictureUrl`)
VALUES
	(1,1,'uploads/rustic-coffee-tables.jpg'),
	(2,1,'uploads/squarecoffeetable.png'),
	(3,2,'uploads/019.ST018-Short-Distressed-Metal-Stool.jpg');

/*!40000 ALTER TABLE `pictures` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `userId` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL DEFAULT '',
  `password` varchar(50) NOT NULL DEFAULT '',
  `userTypeId` int(11) NOT NULL DEFAULT '3',
  PRIMARY KEY (`userId`),
  UNIQUE KEY `uname` (`username`),
  KEY `usertypeid` (`userTypeId`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`usertypeid`) REFERENCES `usertype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;

INSERT INTO `users` (`userId`, `username`, `password`, `userTypeId`)
VALUES
	(1,'admin','password',1);

/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table usertype
# ------------------------------------------------------------

DROP TABLE IF EXISTS `usertype`;

CREATE TABLE `usertype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userType` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `usertype` WRITE;
/*!40000 ALTER TABLE `usertype` DISABLE KEYS */;

INSERT INTO `usertype` (`id`, `userType`)
VALUES
	(1,'admin'),
	(2,'tech'),
	(3,'member');

/*!40000 ALTER TABLE `usertype` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
