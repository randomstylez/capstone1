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
-- Table structure for table `status_subscriber_subservices`
--

DROP TABLE IF EXISTS `status_subscriber_subservices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_subscriber_subservices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subscriber_id` int(11) NOT NULL,
  `subservice_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `status_subscriber_subser_subscriber_id_subservice_83a74955_uniq` (`subscriber_id`,`subservice_id`),
  KEY `status_subscriber_su_subservice_id_e7a6d31e_fk_status_su` (`subservice_id`),
  CONSTRAINT `status_subscriber_su_subscriber_id_735cd139_fk_status_su` FOREIGN KEY (`subscriber_id`) REFERENCES `status_subscriber` (`id`),
  CONSTRAINT `status_subscriber_su_subservice_id_e7a6d31e_fk_status_su` FOREIGN KEY (`subservice_id`) REFERENCES `status_subservice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_subscriber_subservices`
--

LOCK TABLES `status_subscriber_subservices` WRITE;
/*!40000 ALTER TABLE `status_subscriber_subservices` DISABLE KEYS */;
INSERT INTO `status_subscriber_subservices` (`id`, `subscriber_id`, `subservice_id`) VALUES (17,1,90),(16,1,132),(19,5,92),(7,5,132);
/*!40000 ALTER TABLE `status_subscriber_subservices` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-07 16:02:51
