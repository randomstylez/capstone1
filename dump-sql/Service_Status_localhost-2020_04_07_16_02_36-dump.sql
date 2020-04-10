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
-- Table structure for table `status_service`
--

DROP TABLE IF EXISTS `status_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(100) NOT NULL,
  `service_description` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `service_name` (`service_name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_service`
--

LOCK TABLES `status_service` WRITE;
/*!40000 ALTER TABLE `status_service` DISABLE KEYS */;
INSERT INTO `status_service` (`id`, `service_name`, `service_description`) VALUES (1,'100 - Miami - Fortaleza - 01','Node - A:\r\nMIA-MI1-SW01\r\nLocation (Latitude and Longitude): 25.7617° N, 80.1918° W\r\nIP Address: 198.32.252.55\r\nInterface: 7/2\r\nSNMP Community: AAMFM13\r\n\r\nNode - B:\r\nFOR-LAN-SW01\r\nLocation (Latitude and Longitude): 3.7327° S, 38.5270° W\r\nIP address: 190.103.186.218\r\nInterface: 4/1 		\r\nSNMP Community: AAMFM13'),(2,'100 - Fortaleza - São Paulo - 01','Node - A:\r\nFOR-LAN-SW01\r\nLocation (Latitude and Longitude): 3.7327° S, 38.5270° W\r\nIP Address: 190.103.186.218\r\nInterface: 4/2\r\nSNMP Community: AAMFM13\r\n\r\n\r\nNode - B:\r\nSAO-SP4-SW01\r\nLocation (Latitude and Longitude): 23.5505° S, 46.6333° W\r\nIP address: 190.103.186.219\r\nInterface: 6/1\r\nSNMP Community: AAMFM13'),(3,'100 - São Paulo - Santiago - 01','Node - A:\r\nSAO-SP4-SW01\r\nLocation (Latitude and Longitude): 23.5505° S, 46.6333° W\r\nIP Address: 190.103.186.219\r\nInterface: 7/1\r\nSNMP Community: AAMFM13\r\n\r\n\r\nNode - B:\r\nSCL-CLK-SW02\r\nLocation (Latitude and Longitude): 33.4489° S, 70.6693° W\r\nIP address: 190.103.186.220\r\nInterface: 1/25\r\nSNMP Community: AAMFM13'),(4,'100 - Santiago - Panama - 01','Node - A:\r\nSCL-CLK-SW01\r\nLocation (Latitude and Longitude): 33.4489° S, 70.6693° W\r\nIP Address: 190.103.186.221\r\nInterface: 3/1\r\nSNMP Community: AAMFM13\r\n\r\n\r\nNode - B:\r\nPTY-CLK-SW01\r\nLocation (Latitude and Longitude): 8.5380° N, 80.7821° W\r\nIP address: 200.0.205.22\r\nInterface: hu0/1/0/0\r\nSNMP Community: RedCL@R@'),(5,'100 - Panama - San Juan - 01','Node - A:\r\nPTY-CLK-SW01\r\nLocation (Latitude and Longitude): 8.5380° N, 80.7821° W\r\nIP Address: 200.0.205.22\r\nInterface: hu0/1/0/1\r\nSNMP Community: RedCL@R@\r\n\r\n\r\nNode - B:\r\nSJU-H787-SW01\r\nLocation (Latitude and Longitude): 18.2208° N, 66.5901° W\r\nIP address: 190.103.186.222\r\nInterface: 6/1\r\nSNMP Community: AAMFM13'),(6,'100 - San Juan - Miami - 01','Node - A:\r\nSJU-H787-SW01\r\nLocation (Latitude and Longitude): 18.2208° N, 66.5901° W\r\nIP Address: 190.103.186.222\r\nInterface: 5/1\r\nSNMP Community: AAMFM13\r\n\r\n\r\nNode - B:\r\nMIA-MI1-SW02\r\nLocation (Latitude and Longitude): 25.7617° N, 80.1918° W\r\nIP address: 192.32.252.52\r\nInterface: 7/2\r\nSNMP Community: AAMFM13'),(7,'100 - Miami - Fortaleza - 05','Node - A:\r\nMIA-MI1-SW05\r\nLocation (Latitude and Longitude): 25.7617° N, 80.1918° W\r\nIP Address: 198.32.252.54\r\nInterface: 1/31\r\nSNMP Community: AAMFM13\r\n\r\n\r\nNode - B:\r\nFOR-ACB-SW01\r\nLocation (Latitude and Longitude): 3.7327° S, 38.5270° W\r\nIP address: *****\r\nInterface: *****	\r\nSNMP Community: *****'),(8,'100 - Miami - São Paulo - 04','Node - A:\r\nMIA-MI1-SW04\r\nLocation (Latitude and Longitude): 25.7617° N, 80.1918° W\r\nIP Address: 198.32.252.51\r\nInterface: 1/29\r\nSNMP Community: AAMFM13\r\n\r\n\r\nNode - B:\r\nSAO-SP3-SW01\r\nLocation (Latitude and Longitude): 23.5505° S, 46.6333° W\r\nIP address: *****\r\nInterface: 0/1/5\r\nSNMP Community: *****'),(9,'100 - Boca Raton - São Paulo - 01','Node - A:\r\nBCT-MI3-SW01\r\nLocation (Latitude and Longitude): 26.3683° N, 80.1289° W\r\nIP Address: 149.97.166.62\r\nInterface: 1/31\r\nSNMP Community: AAMFM13\r\n\r\n\r\nNode - B:\r\nSAO-SP3-SW01\r\nLocation (Latitude and Longitude): 23.5505° S, 46.6333° W\r\nIP address: *****\r\nInterface: 0/1/9\r\nSNMP Community: *****'),(13,'service - test','description service - test');
/*!40000 ALTER TABLE `status_service` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-07 16:02:36
