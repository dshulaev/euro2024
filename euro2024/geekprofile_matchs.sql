-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: geekprofile
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `matchs`
--

DROP TABLE IF EXISTS `matchs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matchs` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `date` datetime NOT NULL,
  `team1` char(50) NOT NULL,
  `team2` char(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matchs`
--

LOCK TABLES `matchs` WRITE;
/*!40000 ALTER TABLE `matchs` DISABLE KEYS */;
INSERT INTO `matchs` VALUES (3,'2024-06-15 19:00:00','Испания','Хорватия'),(4,'2024-06-15 22:00:00','Италия','Албания'),(5,'2024-06-16 16:00:00','Польша','Нидерланды'),(6,'2024-06-16 19:00:00','Словения','Дания'),(7,'2024-06-16 22:00:00','Сербия','Англия'),(8,'2024-06-17 16:00:00','Румыния','Украина'),(9,'2024-06-17 19:00:00','Бельгия','Словакия'),(10,'2024-06-17 22:00:00','Австрия','Франция'),(11,'2024-06-18 19:00:00','Турция','Грузия'),(12,'2024-06-18 22:00:00','Португалия','Чехия'),(13,'2024-06-19 16:00:00','Хорватия','Албания'),(14,'2024-06-19 19:00:00','Германия','Венгрия'),(15,'2024-06-19 22:00:00','Шотландия','Швейцария'),(16,'2024-06-20 16:00:00','Словения','Сербия'),(17,'2024-06-20 19:00:00','Дания','Англия'),(18,'2024-06-20 22:00:00','Испания','Италия'),(19,'2024-06-21 16:00:00','Словакия','Украина'),(20,'2024-06-21 19:00:00','Польша','Австрия'),(21,'2024-06-21 22:00:00','Нидерланды','Франция'),(22,'2024-06-22 16:00:00','Грузия','Чехия'),(23,'2024-06-21 19:00:00','Турция','Португалия'),(24,'2024-06-21 22:00:00','Бельгия','Румыния'),(25,'2024-06-23 16:00:00','Швейцария','Германия'),(26,'2024-06-23 19:00:00','Шотландия','Венгрия'),(27,'2024-06-24 22:00:00','Албания','Испания'),(28,'2024-06-24 22:00:00','Хорватия','Италия'),(29,'2024-06-25 19:00:00','Нидерланды','Австрия'),(30,'2024-06-25 19:00:00','Франция','Польша'),(31,'2024-06-25 22:00:00','Дания','Сербия'),(32,'2024-06-25 22:00:00','Англия','Словения'),(33,'2024-06-26 19:00:00','Украина','Бельгия'),(34,'2024-06-26 19:00:00','Словакия','Румыния'),(35,'2024-06-26 22:00:00','Грузия','Португалия'),(36,'2024-06-26 22:00:00','Чехия','Турция'),(37,'2024-04-10 22:00:00','Тест','Тест'),(38,'2024-05-15 16:00:00','Тест 2','Тест 2');
/*!40000 ALTER TABLE `matchs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-15 19:57:56
