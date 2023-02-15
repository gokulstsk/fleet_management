-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 15, 2023 at 05:27 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fleet-management`
--

-- --------------------------------------------------------

--
-- Table structure for table `fuel_entry`
--

CREATE TABLE `fuel_entry` (
  `id` int(11) NOT NULL,
  `vehicle` varchar(255) DEFAULT NULL,
  `liters` double DEFAULT NULL,
  `fuel_cost` double DEFAULT NULL,
  `cost_per_liter` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `fuel_entry`
--

INSERT INTO `fuel_entry` (`id`, `vehicle`, `liters`, `fuel_cost`, `cost_per_liter`) VALUES
(1, 'sumo', 12, 12, 12),
(11, 'sumo2', 10, 2000, 200),
(12, 'swift', 23, 134, 12),
(13, 'tata', 10, 134, 200),
(14, 'cruz', 24, 2400, 103);

-- --------------------------------------------------------

--
-- Table structure for table `issue_entry`
--

CREATE TABLE `issue_entry` (
  `id` int(11) NOT NULL,
  `vehicle` varchar(255) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `issue` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `issue_entry`
--

INSERT INTO `issue_entry` (`id`, `vehicle`, `place`, `issue`) VALUES
(1, 'sumo2', 'vennendur', 'wheel punchure'),
(2, 'sumo2', 'asdf', 'asdf'),
(3, 'roce royce', 'vennandur', 'wings not working'),
(4, 'roce royce', 'vennandur', 'wings not working');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `admin_id` int(10) NOT NULL,
  `admin_name` varchar(50) NOT NULL,
  `admin_username` varchar(50) NOT NULL,
  `admin_password` varchar(50) NOT NULL,
  `admin_status` varchar(50) NOT NULL,
  `admin_usertype` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`admin_id`, `admin_name`, `admin_username`, `admin_password`, `admin_status`, `admin_usertype`) VALUES
(1, 'admin', 'admin', 'admin', 'yes', 'data_entry');

-- --------------------------------------------------------

--
-- Table structure for table `trip_entry`
--

CREATE TABLE `trip_entry` (
  `id` int(11) NOT NULL,
  `vehicle` varchar(255) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `start_odometer` varchar(255) DEFAULT NULL,
  `end_odometer` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trip_entry`
--

INSERT INTO `trip_entry` (`id`, `vehicle`, `start_time`, `end_time`, `start_odometer`, `end_odometer`) VALUES
(1, 'sumo', '20:38:40', '23:38:40', '12', '12'),
(21, 'asdf', '20:56:42', '23:56:48', 'asdf', '123'),
(22, 'asdf', '22:00:00', '23:56:02', '123', 'asdf'),
(23, 'cbe', '20:45:24', '01:47:28', '12', '23');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `fuel_entry`
--
ALTER TABLE `fuel_entry`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `issue_entry`
--
ALTER TABLE `issue_entry`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`admin_id`);

--
-- Indexes for table `trip_entry`
--
ALTER TABLE `trip_entry`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `fuel_entry`
--
ALTER TABLE `fuel_entry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `issue_entry`
--
ALTER TABLE `issue_entry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `admin_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `trip_entry`
--
ALTER TABLE `trip_entry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
