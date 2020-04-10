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
-- Table structure for table `status_ticketlog`
--

DROP TABLE IF EXISTS `status_ticketlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_ticketlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_date` datetime(6) NOT NULL,
  `action_notes` longtext,
  `service_history_id` int(11) NOT NULL,
  `service_status_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `status_ticketlog_service_history_id_6fe2b91c_fk_status_ticket_id` (`service_history_id`),
  KEY `status_ticketlog_service_status_id_28439b1d_fk_status_st` (`service_status_id`),
  CONSTRAINT `status_ticketlog_service_history_id_6fe2b91c_fk_status_ticket_id` FOREIGN KEY (`service_history_id`) REFERENCES `status_ticket` (`id`),
  CONSTRAINT `status_ticketlog_service_status_id_28439b1d_fk_status_st` FOREIGN KEY (`service_status_id`) REFERENCES `status_statuscategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_ticketlog`
--

LOCK TABLES `status_ticketlog` WRITE;
/*!40000 ALTER TABLE `status_ticketlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `status_ticketlog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-07 16:03:06
