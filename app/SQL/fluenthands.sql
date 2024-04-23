
-- Create Teacher Table Schema
DROP TABLE IF EXISTS `Teacher`;
CREATE TABLE `Teacher`(
    TeacherID INT NOT NULL AUTO_INCREMENT,
    AccessCode VARCHAR(10) UNIQUE, 
    Fname VARCHAR(50),
    Lname VARCHAR(50),
    Email VARCHAR(80) UNIQUE, -- Email should be unique.
    Pw VARCHAR(128),
    PRIMARY KEY (TeacherID)
);

-- Create Student Table Schema
DROP TABLE IF EXISTS `Student`;
CREATE TABLE `Student`(
    StudentID INT NOT NULL AUTO_INCREMENT,
    Level VARCHAR(50),
    Score INT NOT NULL,
    Fname VARCHAR(50),
    Lname VARCHAR(50),
    Email VARCHAR(80) UNIQUE, 
    Pw VARCHAR(128),
    PRIMARY KEY (StudentID)
);


-- Create Quiz Table Schema
DROP TABLE IF EXISTS `Quiz`;
CREATE TABLE `Quiz`(
    QuizID INT NOT NULL AUTO_INCREMENT,
    Topic VARCHAR(255),
    NumQuestions INT,
    Date DATE,
    CustomQS BOOLEAN,
    TeacherID INT,
    PRIMARY KEY (QuizID),
    FOREIGN KEY (TeacherID) REFERENCES `Teacher`(TeacherID)
);

-- Create Enrol Table Schema
DROP TABLE IF EXISTS `Enrol`;
CREATE TABLE `Enrol`(
    EnrolID INT NOT NULL AUTO_INCREMENT,
    AccessCode VARCHAR(10) NOT NULL,
    StudentID INT NOT NULL,
    PRIMARY KEY (EnrolID),
    FOREIGN KEY (AccessCode) REFERENCES `Teacher`(AccessCode),
    FOREIGN KEY (StudentID) REFERENCES `Student`(StudentID)
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
    TeacherID INT,
    PRIMARY KEY (ImgQuestionID),
    FOREIGN KEY (QuizID) REFERENCES `Quiz`(QuizID),
    FOREIGN KEY (TeacherID) REFERENCES `Teacher`(TeacherID)
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
    TeacherID INT,
    PRIMARY KEY (CamQuestionID),
    FOREIGN KEY (QuizID) REFERENCES `Quiz`(QuizID),
    FOREIGN KEY (TeacherID) REFERENCES `Teacher`(TeacherID)
);

-- Create Leaderboard Table Schema
DROP TABLE IF EXISTS `Leaderboard`;
CREATE TABLE `Leaderboard`(
    LboardID INT NOT NULL AUTO_INCREMENT,
    Score INT,
    StudentID INT,
    TeacherID INT,
    PRIMARY KEY (LboardID),
    FOREIGN KEY (StudentID) REFERENCES `Student`(StudentID),
    FOREIGN KEY (TeacherID) REFERENCES `Teacher`(TeacherID)
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

-- Create Administered Table Schema
DROP TABLE IF EXISTS `Administered`;
CREATE TABLE `Administered`(
    StudentID INT NOT NULL,
    QuizID INT NOT NULL,
    Score INT NOT NULL,
    Feedback TEXT,
    FOREIGN KEY (StudentID) REFERENCES `Student`(StudentID),
    FOREIGN KEY (QuizID) REFERENCES `Quiz`(QuizID)
);


-- ImageBank Table Schema
DROP TABLE IF EXISTS `ImageBank`;
CREATE TABLE `ImageBank` (
    BankID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (BankID)
);

-- Administered Table Schema
DROP TABLE IF EXISTS `Administered`;
CREATE TABLE `Administered` (
    StudentID INT NOT NULL,
    QuizID INT NOT NULL,
    Score INT NOT NULL,
    Feedback TEXT,
    FOREIGN KEY (StudentID) REFERENCES `Student` (StudentID),
    FOREIGN KEY (QuizID) REFERENCES `Quiz` (QuizID)
);

-- View Table Schema
DROP TABLE IF EXISTS `View`;
CREATE TABLE `View` (
    StudentID INT NOT NULL,
    LboardID INT NOT NULL,
    FOREIGN KEY (StudentID) REFERENCES `Student` (StudentID),
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
