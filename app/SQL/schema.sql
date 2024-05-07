-- Database Creation 
DROP DATABASE IF EXISTS fluenthands;
CREATE DATABASE fluenthands;
USE fluenthands;

-- Create Administrator Table Schema
DROP TABLE IF EXISTS `Administrator`;
CREATE TABLE `Administrator`(
    AdminID INT NOT NULL AUTO_INCREMENT,
    AccessCode VARCHAR(7) UNIQUE, 
    Fname VARCHAR(50),
    Lname VARCHAR(50),
    Email VARCHAR(80) UNIQUE, -- Email should be unique.
    Pw VARCHAR(128),
    PRIMARY KEY (AdminID)
);

-- Create a stored procedure to generate random access codes
DROP PROCEDURE IF EXISTS GenerateAccessCode;
DELIMITER //

CREATE PROCEDURE GenerateAccessCode(OUT generated_code VARCHAR(7))
BEGIN
    DECLARE code_first_part VARCHAR(3);
    DECLARE code_second_part VARCHAR(3);
    DECLARE letters VARCHAR(52);
    DECLARE i INT;

    SET letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'; -- Set of letters

    -- Generate the first part of the code
    SET code_first_part = '';
    SET i = 1;
    WHILE i <= 3 DO
        SET code_first_part = CONCAT(code_first_part, SUBSTRING(letters, FLOOR(RAND() * 52) + 1, 1));
        SET i = i + 1;
    END WHILE;

    -- Generate the second part of the code
    SET code_second_part = '';
    SET i = 1;
    WHILE i <= 3 DO
        SET code_second_part = CONCAT(code_second_part, SUBSTRING(letters, FLOOR(RAND() * 52) + 1, 1));
        SET i = i + 1;
    END WHILE;

    -- Set the generated code
    SET generated_code = CONCAT(code_first_part, '-', code_second_part);
END //

DELIMITER ;
-- Create trigger to automatically generate access code when inserting a new administrator
DROP TRIGGER IF EXISTS Before_Insert_Administrator;
DELIMITER //

CREATE TRIGGER Before_Insert_Administrator
BEFORE INSERT ON Administrator
FOR EACH ROW
BEGIN
    SET NEW.AccessCode = @access_code ;
END //

DELIMITER ;

-- Create Participant Table Schema
DROP TABLE IF EXISTS `Participant`;
CREATE TABLE `Participant`(
    ParticipantID INT NOT NULL AUTO_INCREMENT,
    Level VARCHAR(50),
    Score INT NOT NULL,
    Fname VARCHAR(50),
    Lname VARCHAR(50),
    Email VARCHAR(80) UNIQUE, 
    Pw VARCHAR(128),
    PRIMARY KEY (ParticipantID)
);

-- Create Quiz Table Schema
DROP TABLE IF EXISTS `Quiz`;
CREATE TABLE `Quiz`(
    QuizID INT NOT NULL AUTO_INCREMENT,
    Topic VARCHAR(255),
    NumQuestions INT,
    Date DATE,
    CustomQS BOOLEAN,
    AdminID INT,
    PRIMARY KEY (QuizID),
    FOREIGN KEY (AdminID) REFERENCES `Administrator`(AdminID)
);

-- Create Enrol Table Schema
DROP TABLE IF EXISTS `Enrol`;
CREATE TABLE `Enrol`(
    EnrolID INT NOT NULL AUTO_INCREMENT,
    AccessCode VARCHAR(10) NOT NULL,
    ParticipantID INT NOT NULL,
    PRIMARY KEY (EnrolID),
    FOREIGN KEY (AccessCode) REFERENCES `Administrator`(AccessCode),
    FOREIGN KEY (ParticipantID) REFERENCES `Participant`(ParticipantID)
);

-- Create ImageQuestion Table Schema
DROP TABLE IF EXISTS `ImageQuestion`;
CREATE TABLE `ImageQuestion`(
    ImgQuestionID INT NOT NULL AUTO_INCREMENT,
    Topic VARCHAR(255),
    Label VARCHAR(255),
    Marks INT,
    Level VARCHAR(255),
    Path TEXT,
    QuizID INT,
    AdminID INT,
    PRIMARY KEY (ImgQuestionID),
    FOREIGN KEY (QuizID) REFERENCES `Quiz`(QuizID),
    FOREIGN KEY (AdminID) REFERENCES `Administrator`(AdminID)
);

-- Create CamQuestion Table Schema
DROP TABLE IF EXISTS `CamQuestion`;
CREATE TABLE `CamQuestion`(
    CamQuestionID INT NOT NULL AUTO_INCREMENT,
    Topic VARCHAR(255),
    Label VARCHAR(255),
    Marks INT,
    Level VARCHAR(255),
    QuizID INT,
    AdminID INT,
    PRIMARY KEY (CamQuestionID),
    FOREIGN KEY (QuizID) REFERENCES `Quiz`(QuizID),
    FOREIGN KEY (AdminID) REFERENCES `Administrator`(AdminID)
);

-- Create Leaderboard Table Schema
DROP TABLE IF EXISTS `Leaderboard`;
CREATE TABLE `Leaderboard`(
    LboardID INT NOT NULL AUTO_INCREMENT,
    Score INT,
    ParticipantID INT,
    AdminID INT,
    PRIMARY KEY (LboardID),
    FOREIGN KEY (ParticipantID) REFERENCES `Participant`(ParticipantID),
    FOREIGN KEY (AdminID) REFERENCES `Administrator`(AdminID)
);

-- Create ImageBank Table Schema
DROP TABLE IF EXISTS `ImageBank`;
CREATE TABLE `ImageBank`(
    BankID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (BankID)
);

-- Create CamBank Table Schema
DROP TABLE IF EXISTS `CamBank`;
CREATE TABLE `CamBank`(
    BankID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (BankID)
);

-- Administered Table Schema
DROP TABLE IF EXISTS `Administered`;
CREATE TABLE `Administered` (
    ParticipantID INT NOT NULL,
    QuizID INT NOT NULL,
    Score INT NOT NULL,
    Feedback TEXT,
    FOREIGN KEY (ParticipantID) REFERENCES `Participant` (ParticipantID),
    FOREIGN KEY (QuizID) REFERENCES `Quiz` (QuizID)
);

-- View Table Schema
DROP TABLE IF EXISTS `View`;
CREATE TABLE `View` (
    ParticipantID INT NOT NULL,
    LboardID INT NOT NULL,
    FOREIGN KEY (ParticipantID) REFERENCES `Participant` (ParticipantID),
    FOREIGN KEY (LboardID) REFERENCES `Leaderboard` (LboardID)
);

-- Cache Table Schema
DROP TABLE IF EXISTS `Cache`;
CREATE TABLE `Cache` (
    ImgQuestionID INT NOT NULL,
    BankID INT NOT NULL,
    FOREIGN KEY (ImgQuestionID) REFERENCES `ImageQuestion` (ImgQuestionID),
    FOREIGN KEY (BankID) REFERENCES `ImageBank` (BankID)
);

-- LinkedTo Table Schema
DROP TABLE IF EXISTS `LinkedTo`;
CREATE TABLE `LinkedTo` (
    QuizID INT NOT NULL,
    BankID INT NOT NULL,
    FOREIGN KEY (QuizID) REFERENCES `Quiz` (QuizID),
    FOREIGN KEY (BankID) REFERENCES `ImageBank` (BankID)
);

-- Insert queries ----------------------------------------------------------------------
-- Administrator Queries
CALL GenerateAccessCode(@access_code);
INSERT INTO Administrator (AccessCode, Fname, Lname, Email, Pw) VALUES (@access_code, 'Michele', 'Matthews', 'petersonalicia@gmail.com', '3MM3G2zSrt');
CALL GenerateAccessCode(@access_code);
INSERT INTO Administrator (AccessCode, Fname, Lname, Email, Pw) VALUES (@access_code, 'Mark', 'Daniels', 'devin68@gmail.com', '4IMCqpEcCU');
CALL GenerateAccessCode(@access_code);
INSERT INTO Administrator (AccessCode, Fname, Lname, Email, Pw) VALUES (@access_code, 'Erica', 'Hernandez', 'tarabaker@gmail.com', 'M7QxHNFhxw');
CALL GenerateAccessCode(@access_code);
INSERT INTO Administrator (AccessCode, Fname, Lname, Email, Pw) VALUES (@access_code, 'Miranda', 'Gilmore', 'anthony63@gmail.com', '7cfo0G9pf0');
CALL GenerateAccessCode(@access_code);
INSERT INTO Administrator (AccessCode, Fname, Lname, Email, Pw) VALUES (@access_code, 'Eric', 'Lee', 'debra10@gmail.com', 'aYEFrdUZ4D');
CALL GenerateAccessCode(@access_code);
INSERT INTO Administrator (AccessCode, Fname, Lname, Email, Pw) VALUES (@access_code, 'Christopher', 'Brown', 'mckayjonathan@gmail.com', 'qFROuH0P2E');
CALL GenerateAccessCode(@access_code);
INSERT INTO Administrator (AccessCode, Fname, Lname, Email, Pw) VALUES (@access_code, 'Ethan', 'Hancock', 'jason22@gmail.com', 'O6hl6NFvMu');
CALL GenerateAccessCode(@access_code);
INSERT INTO Administrator (AccessCode, Fname, Lname, Email, Pw) VALUES (@access_code, 'Ronald', 'Bishop', 'nathan53@gmail.com', 'qEoYc27h3E');
CALL GenerateAccessCode(@access_code);
INSERT INTO Administrator (AccessCode, Fname, Lname, Email, Pw) VALUES (@access_code, 'Walter', 'Vega', 'bward@gmail.com', 'ZL38PCyTec');
CALL GenerateAccessCode(@access_code);
INSERT INTO Administrator (AccessCode, Fname, Lname, Email, Pw) VALUES (@access_code, 'Julie', 'Tran', 'katelynramirez@gmail.com', 'm4dMNWqIkg');

-- Quizzes Queries
INSERT INTO Quiz (Topic, NumQuestions, Date, CustomQS, AdminID) VALUES ('Alphabet', 5, '2024-04-28', 0, 8);
INSERT INTO Quiz (Topic, NumQuestions, Date, CustomQS, AdminID) VALUES ('Alphabet', 8, '2023-09-11', 0, 7);
INSERT INTO Quiz (Topic, NumQuestions, Date, CustomQS, AdminID) VALUES ('Alphabet', 12, '2023-05-24', 0, 10);