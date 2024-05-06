-- Database Creation 
DROP DATABASE IF EXISTS fluenthands;
CREATE DATABASE fluenthands;
USE fluenthands;

-- ----------------------- USERS -----------------------
-- Create Administrator Table Schema
DROP TABLE IF EXISTS `Administrator`;
CREATE TABLE `Administrator`(
    AdminID INT NOT NULL AUTO_INCREMENT,
    AccessCode VARCHAR(10) UNIQUE, 
    Fname VARCHAR(50),
    Lname VARCHAR(50),
    Email VARCHAR(80) UNIQUE, -- Email should be unique.
    Pw VARCHAR(128),
    PRIMARY KEY (AdminID)
);

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
    FOREIGN KEY (BankID) REFERENCES `ImageBank` (BankID));
