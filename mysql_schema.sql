SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `telegram`;
CREATE DATABASE `telegram` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `telegram`;

DROP TABLE IF EXISTS `chats`;
CREATE TABLE `chats` (
  `uid` bigint NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `data` json NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
  `uid` bigint NOT NULL,
  `path` text COLLATE utf8mb4_general_ci NOT NULL,
  `data` json NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
  `uid` bigint NOT NULL,
  `chat_uid` bigint NOT NULL,
  `type` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `data` json NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
