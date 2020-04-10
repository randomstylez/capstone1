-- MySQL dump 10.13  Distrib 8.0.18, for osx10.15 (x86_64)
--
-- Host: 127.0.0.1    Database: Service-Status
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `status_statuscategory`
--

DROP TABLE IF EXISTS `status_statuscategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_statuscategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status_category_tag` varchar(45) NOT NULL,
  `status_category_color` varchar(7) NOT NULL,
  `status_category_color_hex` varchar(18) NOT NULL,
  `status_class_design` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `status_category_tag` (`status_category_tag`),
  UNIQUE KEY `status_category_color` (`status_category_color`),
  UNIQUE KEY `status_class_design` (`status_class_design`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_statuscategory`
--

LOCK TABLES `status_statuscategory` WRITE;
/*!40000 ALTER TABLE `status_statuscategory` DISABLE KEYS */;
INSERT INTO `status_statuscategory` (`id`, `status_category_tag`, `status_category_color`, `status_category_color_hex`, `status_class_design`) VALUES (1,'In Process','Yellow','#DBBF07','fas fa-tools'),(2,'Alert','Orange','#FC810D','fas fa-exclamation-circle'),(3,'Outage','Red','#F00004','fas fa-times-circle'),(4,'Planned','Blue','#041DBF','far fa-calendar-alt'),(5,'No Issues','Green','#0AC739','fas fa-check-circle');
/*!40000 ALTER TABLE `status_statuscategory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-07 16:02:39
