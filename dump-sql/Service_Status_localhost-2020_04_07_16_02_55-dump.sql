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
-- Table structure for table `status_subservice`
--

DROP TABLE IF EXISTS `status_subservice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `status_subservice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sub_service_name` varchar(100) NOT NULL,
  `sub_service_description` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sub_service_name` (`sub_service_name`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status_subservice`
--

LOCK TABLES `status_subservice` WRITE;
/*!40000 ALTER TABLE `status_subservice` DISABLE KEYS */;
INSERT INTO `status_subservice` (`id`, `sub_service_name`, `sub_service_description`) VALUES (87,'Vlan_2007_AMPATH_RNP - Backup','Backup'),(88,'Vlan_2007_AMPATH_RNP - Primary','Primary'),(89,'Vlan_2008_RedCLARA - Backup','Backup'),(90,'Vlan_2008_RedCLARA - Primary','Primary'),(91,'Vlan_2011_RNP - Backup','Backup'),(92,'Vlan_2011_RNP - Primary','Primary'),(93,'Vlan_3001_RNP_SGO_SPO - Backup','Backup'),(94,'Vlan_3002_RNP_SGO_MIA - Backup','Backup'),(95,'Vlan_3002_RNP_SGO_MIA - Primary','Primary'),(96,'Vlan_3005_RNP - Backup','Backup'),(97,'Vlan_3005_RNP - Primary','Primary'),(98,'Vlan_3008_RNP - Primary','Primary'),(99,'Vlan_3015_RNP - Backup','Backup'),(100,'Vlan_3015_RNP - Primary','Primary'),(101,'Vlan_340_LSST_DTN_AMPATH - Backup','Backup'),(102,'Vlan_340_LSST_DTN_AMPATH - Primary','Primary'),(103,'Vlan_473_RNP-ESNet - Backup','Backup'),(104,'Vlan_473_RNP-ESNet - Primary','Primary'),(105,'Vlan_612_RedCLARA_GEANT - Backup','Backup'),(106,'Vlan_612_RedCLARA_GEANT - Primary','Primary'),(107,'Vlan_811_RedCLARA - Backup','Backup'),(108,'Vlan_811_RedCLARA - Primary','Primary'),(109,'Vlan_814_RedCLARA - Primary','Primary'),(110,'Vlan_814_UPR_Commodity - Backup','Backup'),(111,'Vlan_814_UPR_Commodity - Primary','Primary'),(112,'Vlan_815_RedCLARA - Primary','Primary'),(113,'Vlan_815_UPR_Academic - Backup','Backup'),(114,'Vlan_815_UPR_Academic - Primary','Primary'),(115,'Vlan_816_RedCLARA - Primary','Primary'),(116,'Vlan_816_UPR_Commodity - Backup','Backup'),(117,'Vlan_816_UPR_Commodity - Primary','Primary'),(118,'Vlan_817_UPR_Academic - Backup','Backup'),(119,'Vlan_817_UPR_Academic - Primary','Primary'),(120,'Vlan_821_RedCLARA - Primary','Primary'),(121,'Vlan_870_RedCLARA - Backup','Backup'),(122,'Vlan_872_RedCLARA - Primary','Primary'),(123,'Vlan_88_465_RedCLARA - Backup','Backup'),(124,'Vlan_88_465_RedCLARA - Primary','Primary'),(125,'Vlan_956_RedCLARA - Primary','Primary'),(132,'subservice - test','Description of sub-service test');
/*!40000 ALTER TABLE `status_subservice` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-07 16:02:55
