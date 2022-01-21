USE `flask`;

CREATE TABLE `College` (
    `college_code` VARCHAR(10),
    `college_name` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`college_code`)
);

CREATE TABLE `Course` (
    `course_code` VARCHAR(10) PRIMARY KEY,
    `course_name` VARCHAR(50) NOT NULL,
    `college` VARCHAR(10) NOT NULL,
    FOREIGN KEY (`college`) REFERENCES `College` (`college_code`)
);

CREATE TABLE `Student` (
    `id_number` VARCHAR(9) PRIMARY KEY,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `course` VARCHAR(10) NOT NULL,
    `year_level` VARCHAR(10) NOT NULL,
    `gender` VARCHAR(25) NOT NULL,
    `profile_pic` VARCHAR(225) NOT NULL,
    
    FOREIGN KEY (`course`) REFERENCES `Course` (`course_code`)
);

INSERT INTO `College` VALUES ("CCS", "College of Computer Studies");
INSERT INTO `Course` VALUES ("BSCS", "BS in Computer Science", "CCS");
INSERT INTO `Course` VALUES ("BSCA", "BS in Computer Applications", "CCS");
INSERT INTO `Course` VALUES ("BSIT", "BS in Information Technology", "CCS");
INSERT INTO `Course` VALUES ("BSIS", "BS in Information Systems", "CCS");
INSERT INTO `Student` VALUES ("2019-4223", "Angelique Joy", "Cañete", "BSCS", 3, "Female");
