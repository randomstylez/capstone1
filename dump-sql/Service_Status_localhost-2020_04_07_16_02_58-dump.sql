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
-- Table structure for table `status_subserviceservices`
--

DROP TABLE IF EXISTS `status_subserviceservices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_subserviceservices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `priority_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `subservice_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `status_subserviceservices_service_id_subservice_id_e33b8a62_uniq` (`service_id`,`subservice_id`),
  KEY `status_subserviceser_priority_id_4e5d3990_fk_status_pr` (`priority_id`),
  KEY `status_subserviceser_subservice_id_1cb06bd9_fk_status_su` (`subservice_id`),
  CONSTRAINT `status_subserviceser_priority_id_4e5d3990_fk_status_pr` FOREIGN KEY (`priority_id`) REFERENCES `status_priority` (`id`),
  CONSTRAINT `status_subserviceser_service_id_bf780dd3_fk_status_se` FOREIGN KEY (`service_id`) REFERENCES `status_service` (`id`),
  CONSTRAINT `status_subserviceser_subservice_id_1cb06bd9_fk_status_su` FOREIGN KEY (`subservice_id`) REFERENCES `status_subservice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=289 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_subserviceservices`
--

LOCK TABLES `status_subserviceservices` WRITE;
/*!40000 ALTER TABLE `status_subserviceservices` DISABLE KEYS */;
INSERT INTO `status_subserviceservices` (`id`, `priority_id`, `service_id`, `subservice_id`) VALUES (184,5,3,89),(185,5,3,91),(186,5,3,93),(187,5,3,94),(188,5,3,96),(189,5,3,99),(190,5,3,101),(191,5,3,103),(192,5,3,105),(193,5,3,107),(194,1,3,109),(195,1,3,112),(196,1,3,115),(197,5,3,116),(198,5,3,118),(199,1,3,120),(200,5,3,123),(201,1,3,125),(202,5,3,87),(203,1,1,88),(204,1,1,90),(205,1,1,92),(206,5,1,93),(207,1,1,95),(208,1,1,97),(209,1,1,98),(210,1,1,100),(211,5,1,101),(212,1,1,104),(213,1,1,106),(214,1,1,108),(215,5,1,116),(216,5,1,118),(217,1,1,124),(218,1,2,88),(219,1,2,90),(220,1,2,92),(221,5,2,93),(222,1,2,95),(223,1,2,97),(224,1,2,98),(225,1,2,100),(226,5,2,101),(227,1,2,104),(228,1,2,106),(229,1,2,108),(230,5,2,116),(231,5,2,118),(232,1,2,124),(233,5,6,87),(234,5,6,89),(235,5,6,91),(236,5,6,93),(237,5,6,94),(238,5,6,96),(239,5,6,99),(240,1,6,102),(241,5,6,103),(242,5,6,105),(243,5,6,107),(244,1,6,111),(245,1,6,114),(246,1,6,117),(247,1,6,119),(248,5,6,121),(249,1,6,122),(250,5,6,123),(251,5,4,87),(252,5,4,89),(253,5,4,91),(254,5,4,93),(255,5,4,94),(256,5,4,96),(257,5,4,99),(258,1,4,102),(259,5,4,103),(260,5,4,105),(261,5,4,107),(262,5,4,110),(263,5,4,113),(264,5,4,116),(265,5,4,118),(266,5,4,121),(267,5,4,123),(268,5,5,87),(269,5,5,89),(270,5,5,91),(271,5,5,93),(272,5,5,94),(273,5,5,96),(274,5,5,99),(275,1,5,102),(276,5,5,103),(277,5,5,105),(278,5,5,107),(279,5,5,110),(280,5,5,113),(281,5,5,116),(282,5,5,118),(283,5,5,121),(284,5,5,123),(288,1,13,132);
/*!40000 ALTER TABLE `status_subserviceservices` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-07 16:02:58
