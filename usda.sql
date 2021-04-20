CREATE DATABASE  IF NOT EXISTS `usda` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `usda`;
-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: usda
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Table structure for table `data_src`
--

DROP TABLE IF EXISTS `data_src`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_src` (
  `DataSrc_ID` varchar(6) NOT NULL,
  `Authors` varchar(255) DEFAULT NULL,
  `Title` varchar(255) NOT NULL,
  `Year` varchar(4) DEFAULT NULL,
  `Journal` varchar(135) DEFAULT NULL,
  `Vol_City` varchar(16) DEFAULT NULL,
  `Issue_State` varchar(5) DEFAULT NULL,
  `Start_Page` varchar(5) DEFAULT NULL,
  `End_Page` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `datsrcln`
--

DROP TABLE IF EXISTS `datsrcln`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datsrcln` (
  `NDB_No` varchar(5) NOT NULL,
  `Nutr_No` varchar(3) NOT NULL,
  `DataSrc_ID` varchar(6) NOT NULL,
  PRIMARY KEY (`NDB_No`,`Nutr_No`,`DataSrc_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `deriv_cd`
--

DROP TABLE IF EXISTS `deriv_cd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deriv_cd` (
  `Deriv_Cd` varchar(4) NOT NULL,
  `Deric_Desc` varchar(120) NOT NULL,
  PRIMARY KEY (`Deriv_Cd`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fd_group`
--

DROP TABLE IF EXISTS `fd_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fd_group` (
  `FdGrp_Cd` varchar(4) NOT NULL,
  `FdGrp_Desc` varchar(60) NOT NULL,
  PRIMARY KEY (`FdGrp_Cd`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `food_des`
--

DROP TABLE IF EXISTS `food_des`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_des` (
  `NDB_No` varchar(5) NOT NULL,
  `FdGrp_Cd` varchar(4) NOT NULL,
  `Long_Desc` varchar(200) NOT NULL,
  `Shrt_Desc` varchar(60) NOT NULL,
  `ComName` varchar(100) DEFAULT NULL,
  `ManufacName` varchar(65) DEFAULT NULL,
  `Survey` varchar(1) DEFAULT NULL,
  `Ref_desc` varchar(135) DEFAULT NULL,
  `Refuse` int DEFAULT NULL,
  `SciName` varchar(65) DEFAULT NULL,
  `N_Factor` decimal(6,2) DEFAULT NULL,
  `Pro_Factor` decimal(6,2) DEFAULT NULL,
  `Fat_Factor` decimal(6,2) DEFAULT NULL,
  `CHO_Factor` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`NDB_No`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `footnote`
--

DROP TABLE IF EXISTS `footnote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `footnote` (
  `NDB_No` varchar(5) NOT NULL,
  `Footnt_No` varchar(4) NOT NULL,
  `Footnt_Typ` varchar(1) NOT NULL,
  `Nutr_No` varchar(3) DEFAULT NULL,
  `Footnt_Txt` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `langdesc`
--

DROP TABLE IF EXISTS `langdesc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `langdesc` (
  `Factor_Code` varchar(5) DEFAULT NULL,
  `Description` varchar(140) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `langual`
--

DROP TABLE IF EXISTS `langual`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `langual` (
  `NDB_No` varchar(5) NOT NULL,
  `Factor_Code` varchar(5) NOT NULL,
  PRIMARY KEY (`NDB_No`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nut_data`
--

DROP TABLE IF EXISTS `nut_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nut_data` (
  `NDB_No` varchar(5) NOT NULL,
  `Nutr_No` varchar(3) NOT NULL,
  `Nutr_Val` decimal(13,3) NOT NULL,
  `Num_Data_Ptr` decimal(10,0) NOT NULL,
  `Std_Error` decimal(11,3) DEFAULT NULL,
  `Src_Cd` varchar(2) NOT NULL,
  `Deriv_cd` varchar(4) DEFAULT NULL,
  `Ref_NDB_No` varchar(5) DEFAULT NULL,
  `Add_Nutr_Mark` varchar(1) DEFAULT NULL,
  `Num_Studies` int DEFAULT NULL,
  `Min` decimal(13,3) DEFAULT NULL,
  `Max` decimal(13,3) DEFAULT NULL,
  `DF` int DEFAULT NULL,
  `Low_EB` decimal(13,3) DEFAULT NULL,
  `Up_EB` decimal(13,3) DEFAULT NULL,
  `Stat_cmd` varchar(10) DEFAULT NULL,
  `AddMod_Date` varchar(10) DEFAULT NULL,
  `CC` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`NDB_No`,`Nutr_No`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `nutr_def`
--

DROP TABLE IF EXISTS `nutr_def`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nutr_def` (
  `Nutr_No` varchar(4) NOT NULL,
  `Units` varchar(7) NOT NULL,
  `Tagname` varchar(20) DEFAULT NULL,
  `NutrDesc` varchar(60) NOT NULL,
  `Num_Dec` varchar(1) NOT NULL,
  `SR_Order` int NOT NULL,
  PRIMARY KEY (`Nutr_No`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `src_cd`
--

DROP TABLE IF EXISTS `src_cd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `src_cd` (
  `Src_Cd` varchar(2) NOT NULL,
  `SrcCd_Desc` varchar(60) NOT NULL,
  PRIMARY KEY (`Src_Cd`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `weight`
--

DROP TABLE IF EXISTS `weight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weight` (
  `NDB_No` varchar(5) NOT NULL,
  `Seq` varchar(2) NOT NULL,
  `Amount` decimal(8,3) NOT NULL,
  `Msre_Desc` varchar(84) NOT NULL,
  `Gm_Wgt` decimal(8,1) NOT NULL,
  `Num_Data_Pts` int DEFAULT NULL,
  `Std_Dev` decimal(10,3) DEFAULT NULL,
  PRIMARY KEY (`NDB_No`,`Seq`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'usda'
--

--
-- Dumping routines for database 'usda'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-20  3:25:37
