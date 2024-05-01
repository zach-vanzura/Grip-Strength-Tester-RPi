CREATE TABLE `grip_log` (
  `id` int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `timestamp` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `progress` float NOT NULL
);