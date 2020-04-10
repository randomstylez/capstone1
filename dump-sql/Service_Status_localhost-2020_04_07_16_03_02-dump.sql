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
-- Table structure for table `status_ticket`
--

DROP TABLE IF EXISTS `status_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_ticket` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ticket_id` varchar(10) NOT NULL,
  `begin` datetime(6) NOT NULL,
  `end` datetime(6) DEFAULT NULL,
  `action_description` longtext NOT NULL,
  `action_notes` longtext,
  `notify_action` tinyint(1) NOT NULL,
  `category_status_id` int(11) DEFAULT NULL,
  `sub_service_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ticket_id` (`ticket_id`),
  KEY `status_ticket_category_status_id_755e46bb_fk_status_st` (`category_status_id`),
  KEY `status_ticket_sub_service_id_b2ead5eb_fk_status_subservice_id` (`sub_service_id`),
  CONSTRAINT `status_ticket_category_status_id_755e46bb_fk_status_st` FOREIGN KEY (`category_status_id`) REFERENCES `status_statuscategory` (`id`),
  CONSTRAINT `status_ticket_sub_service_id_b2ead5eb_fk_status_subservice_id` FOREIGN KEY (`sub_service_id`) REFERENCES `status_subservice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_ticket`
--

LOCK TABLES `status_ticket` WRITE;
/*!40000 ALTER TABLE `status_ticket` DISABLE KEYS */;
INSERT INTO `status_ticket` (`id`, `ticket_id`, `begin`, `end`, `action_description`, `action_notes`, `notify_action`, `category_status_id`, `sub_service_id`) VALUES (19,'ITA0001512','2020-03-31 21:09:01.000000','2020-04-07 15:38:59.000000','<p>description ticket 1 test 26xfghxdgfghf</p>','',1,2,132),(23,'ITA0001514','2020-04-02 15:15:03.000000',NULL,'description ticket 3 test 4','',1,2,132),(24,'ITA0001513','2020-04-02 15:16:56.000000',NULL,'sdbfdbxnbxcnbxdfgsfgsdgfsd93','',1,3,132);
/*!40000 ALTER TABLE `status_ticket` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-07 16:03:02
