-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: managecf
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `name` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES ('Cà phê',1),('Trà',2),('Đá xay',3);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `price` float NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `quantity` int NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `category_id` int NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES ('Cà phê Đen','Đậm đà truyền thống',29000,'img/cfden.jpg',88,'2025-12-30 10:49:34',1,1,1),('Cà phê Sữa','Sữa đặc ngôi sao',29000,'img/cfsua.jpg',100,'2025-12-30 10:49:34',1,1,2),('Bạc Xỉu','Nhiều sữa ít cafe',29000,'img/bacxiu.jpg',100,'2025-12-30 10:49:34',1,1,3),('Espresso','Cà phê máy nguyên chất',45000,'img/espresso.jpg',100,'2025-12-30 10:49:34',1,1,4),('Americano','Espresso thêm nước',45000,'img/americano.jpg',100,'2025-12-30 10:49:34',1,1,5),('Trà Thạch Vải','Best seller',45000,'img/trathachvai.jpg',99,'2025-12-30 10:49:34',1,2,6),('Trà Thạch Đào','Thơm ',45000,'img/trathachdao.jpg',99,'2025-12-30 10:49:34',1,2,7),('Trà Sen Vàng','Thanh mát hạt sen',45000,'img/trasenvang.jpg',99,'2025-12-30 10:49:34',1,2,8),('Trà Thanh Đào','Đậm vị trà',45000,'img/trathanhdao.jpg',100,'2025-12-30 10:49:34',1,2,9),('Matcha Đá Xay','Trà xanh Nhật Bản',55000,'img/freezee_tra_xanh.jpg',100,'2025-12-30 10:49:34',1,3,10),('Chocolate Đá Xay','Đắng ngọt hòa quyện',55000,'img/freezee_chocolate.jpg',100,'2025-12-30 10:49:34',1,3,11),('Cappuccino','Cà phê',65000,'img/cappuccino.jpg',100,'2025-12-30 10:49:34',1,1,12),('Latte','Cà phê',65000,'img/latte.jpg',4,'2025-12-30 10:49:34',1,1,13);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt`
--

DROP TABLE IF EXISTS `receipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt` (
  `user_id` int NOT NULL,
  `created_date` datetime DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `receipt_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt`
--

LOCK TABLES `receipt` WRITE;
/*!40000 ALTER TABLE `receipt` DISABLE KEYS */;
INSERT INTO `receipt` VALUES (2,'2025-01-10 09:00:00',1),(2,'2025-01-15 09:00:00',2),(2,'2025-01-20 09:00:00',3),(2,'2025-02-14 09:00:00',4),(2,'2025-02-20 09:00:00',5),(2,'2025-02-28 09:00:00',6),(2,'2025-03-05 09:00:00',7),(2,'2025-03-10 09:00:00',8),(2,'2025-03-15 09:00:00',9),(4,'2025-12-30 11:27:33',10),(4,'2025-12-30 11:34:11',11),(1,'2025-12-30 11:57:29',12),(1,'2025-12-30 11:59:13',13);
/*!40000 ALTER TABLE `receipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receipt_detail`
--

DROP TABLE IF EXISTS `receipt_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receipt_detail` (
  `receipt_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  `unit_price` float DEFAULT NULL,
  PRIMARY KEY (`receipt_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `receipt_detail_ibfk_1` FOREIGN KEY (`receipt_id`) REFERENCES `receipt` (`id`),
  CONSTRAINT `receipt_detail_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receipt_detail`
--

LOCK TABLES `receipt_detail` WRITE;
/*!40000 ALTER TABLE `receipt_detail` DISABLE KEYS */;
INSERT INTO `receipt_detail` VALUES (1,1,2,25000),(1,2,1,29000),(2,3,1,32000),(2,4,2,35000),(3,1,5,25000),(4,10,2,55000),(4,11,2,55000),(5,6,3,45000),(5,7,2,42000),(6,12,2,52000),(7,2,5,29000),(7,6,5,45000),(8,5,2,35000),(8,9,2,35000),(9,13,3,49000),(10,1,1,29000),(10,6,1,45000),(10,7,1,45000),(10,8,1,45000),(11,1,11,29000),(12,1,1,29000),(12,6,3,45000),(13,1,1,29000),(13,3,12,29000),(13,6,3,45000);
/*!40000 ALTER TABLE `receipt_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `phone_number` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avatar` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `join_date` datetime DEFAULT NULL,
  `user_role` enum('ADMIN','USER') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('Quản trị viên','admin','202cb962ac59075b964b07152d234b70','admin@dcoffee.com',NULL,NULL,1,'2025-12-30 10:49:34','ADMIN',1),('Khách vãng lai','guest','202cb962ac59075b964b07152d234b70',NULL,NULL,NULL,1,'2025-12-30 10:49:34','USER',2),('abc','user1','202cb962ac59075b964b07152d234b70','',NULL,NULL,1,'2025-12-30 10:52:44','USER',3),('Cappuccino','asd','202cb962ac59075b964b07152d234b70','',NULL,NULL,1,'2025-12-30 11:22:53','USER',4);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-30 14:21:31
