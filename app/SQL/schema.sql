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
INSERT INTO Quiz (Topic, NumQuestions, Date, CustomQS, AdminID) VALUES ('Alphabet', '9', '2023-09-07', '1', '10');
INSERT INTO Quiz (Topic, NumQuestions, Date, CustomQS, AdminID) VALUES ('Alphabet', '24', '2024-03-24', '1', '10');
INSERT INTO Quiz (Topic, NumQuestions, Date, CustomQS, AdminID) VALUES ('Alphabet', '25', '2023-12-26', '1', '7');


-- ImageQuestions Queries
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'Q', '7', 'Pro', 'imageQuestions/Alphabet/Q.png', '1', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'I', '7', 'Pro', 'imageQuestions/Alphabet/I.png', '1', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'F', '9', 'Intermediate', 'imageQuestions/Alphabet/F.png', '1', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'U', '3', 'Intermediate', 'imageQuestions/Alphabet/U.png', '1', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'W', '10', 'Beginner', 'imageQuestions/Alphabet/W.png', '1', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'V', '2', 'Beginner', 'imageQuestions/Alphabet/V.png', '1', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'W', '7', 'Intermediate', 'imageQuestions/Alphabet/W.png', '1', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'C', '6', 'Pro', 'imageQuestions/Alphabet/C.png', '1', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'U', '5', 'Pro', 'imageQuestions/Alphabet/U.png', '1', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'M', '5', 'Intermediate', 'imageQuestions/Alphabet/M.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'P', '4', 'Pro', 'imageQuestions/Alphabet/P.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'G', '8', 'Intermediate', 'imageQuestions/Alphabet/G.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'Z', '7', 'Intermediate', 'imageQuestions/Alphabet/Z.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'Z', '5', 'Intermediate', 'imageQuestions/Alphabet/Z.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'S', '7', 'Beginner', 'imageQuestions/Alphabet/S.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'F', '6', 'Pro', 'imageQuestions/Alphabet/F.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'D', '9', 'Pro', 'imageQuestions/Alphabet/D.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'G', '1', 'Intermediate', 'imageQuestions/Alphabet/G.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'I', '1', 'Pro', 'imageQuestions/Alphabet/I.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'Y', '3', 'Intermediate', 'imageQuestions/Alphabet/Y.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'O', '7', 'Pro', 'imageQuestions/Alphabet/O.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'D', '3', 'Intermediate', 'imageQuestions/Alphabet/D.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'D', '6', 'Intermediate', 'imageQuestions/Alphabet/D.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'Z', '7', 'Pro', 'imageQuestions/Alphabet/Z.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'Q', '6', 'Pro', 'imageQuestions/Alphabet/Q.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'H', '6', 'Pro', 'imageQuestions/Alphabet/H.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'J', '2', 'Pro', 'imageQuestions/Alphabet/J.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'L', '4', 'Beginner', 'imageQuestions/Alphabet/L.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'V', '7', 'Pro', 'imageQuestions/Alphabet/V.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'G', '1', 'Pro', 'imageQuestions/Alphabet/G.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'H', '6', 'Pro', 'imageQuestions/Alphabet/H.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'B', '9', 'Intermediate', 'imageQuestions/Alphabet/B.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'V', '3', 'Intermediate', 'imageQuestions/Alphabet/V.png', '2', '10');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'V', '6', 'Beginner', 'imageQuestions/Alphabet/V.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'W', '9', 'Intermediate', 'imageQuestions/Alphabet/W.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'Q', '1', 'Pro', 'imageQuestions/Alphabet/Q.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'K', '9', 'Beginner', 'imageQuestions/Alphabet/K.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'V', '5', 'Intermediate', 'imageQuestions/Alphabet/V.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'D', '1', 'Intermediate', 'imageQuestions/Alphabet/D.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'H', '8', 'Pro', 'imageQuestions/Alphabet/H.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'E', '2', 'Beginner', 'imageQuestions/Alphabet/E.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'T', '2', 'Beginner', 'imageQuestions/Alphabet/T.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'Y', '2', 'Beginner', 'imageQuestions/Alphabet/Y.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'X', '7', 'Beginner', 'imageQuestions/Alphabet/X.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'S', '9', 'Pro', 'imageQuestions/Alphabet/S.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'R', '6', 'Pro', 'imageQuestions/Alphabet/R.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'Z', '8', 'Intermediate', 'imageQuestions/Alphabet/Z.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'B', '3', 'Beginner', 'imageQuestions/Alphabet/B.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'A', '10', 'Pro', 'imageQuestions/Alphabet/A.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'N', '2', 'Pro', 'imageQuestions/Alphabet/N.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'R', '7', 'Beginner', 'imageQuestions/Alphabet/R.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'E', '6', 'Intermediate', 'imageQuestions/Alphabet/E.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'J', '4', 'Pro', 'imageQuestions/Alphabet/J.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'D', '2', 'Beginner', 'imageQuestions/Alphabet/D.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'I', '4', 'Intermediate', 'imageQuestions/Alphabet/I.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'E', '2', 'Intermediate', 'imageQuestions/Alphabet/E.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'L', '1', 'Intermediate', 'imageQuestions/Alphabet/L.png', '3', '7');
INSERT INTO ImageQuestion (Topic, Label, Marks, Level, Path, QuizID, AdminID) VALUES ('Alphabet', 'B', '4', 'Pro', 'imageQuestions/Alphabet/B.png', '3', '7');
