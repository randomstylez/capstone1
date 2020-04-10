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
-- Table structure for table `status_region_services`
--

DROP TABLE IF EXISTS `status_region_services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_region_services` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `status_region_services_region_id_service_id_3b3bdea0_uniq` (`region_id`,`service_id`),
  KEY `status_region_services_service_id_185c1455_fk_status_service_id` (`service_id`),
  CONSTRAINT `status_region_services_region_id_29efcbcb_fk_status_region_id` FOREIGN KEY (`region_id`) REFERENCES `status_region` (`id`),
  CONSTRAINT `status_region_services_service_id_185c1455_fk_status_service_id` FOREIGN KEY (`service_id`) REFERENCES `status_service` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_region_services`
--

LOCK TABLES `status_region_services` WRITE;
/*!40000 ALTER TABLE `status_region_services` DISABLE KEYS */;
INSERT INTO `status_region_services` (`id`, `region_id`, `service_id`) VALUES (18,1,1),(14,1,2),(15,1,3),(16,1,4),(2,1,5),(3,1,6),(4,2,1),(5,2,2),(6,2,3),(19,2,4),(20,2,5),(21,2,6),(22,3,1),(23,3,2),(24,3,3),(25,3,4),(7,3,5),(8,3,6),(26,6,1),(27,6,2),(28,6,3),(29,6,4),(30,6,5),(31,6,6),(35,7,1),(36,7,2),(37,7,3),(32,7,4),(33,7,5),(34,7,6);
/*!40000 ALTER TABLE `status_region_services` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-07 16:02:32
