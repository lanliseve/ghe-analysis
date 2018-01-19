-- MySQL Script generated by MySQL Workbench
-- Tue Aug  1 16:39:44 2017
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema github
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `github` ;

-- -----------------------------------------------------
-- Schema github
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `github` DEFAULT CHARACTER SET latin1 ;
USE `github` ;

-- -----------------------------------------------------
-- Table `github`.`app_account_owner`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`app_account_owner` ;

CREATE TABLE IF NOT EXISTS `github`.`app_account_owner` (
  `instance` VARCHAR(50) NOT NULL,
  `login` VARCHAR(100) NOT NULL,
  `owner_uid` VARCHAR(100) NOT NULL,
  `owner_hpStatus` VARCHAR(100) NULL DEFAULT NULL,
  `owner_hpeSpinCompany` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`instance`, `login`, `owner_uid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

-- -----------------------------------------------------
-- Table `github`.`user_commit_contributions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`user_commit_contributions` ;

CREATE TABLE IF NOT EXISTS `github`.`user_commit_contributions` (
  `instance` VARCHAR(50) NOT NULL,
  `login` VARCHAR(100) NOT NULL,
  `committed_date` DATETIME NULL DEFAULT NULL,
  `repo_id` INT(11) NULL DEFAULT NULL,
 PRIMARY KEY (`instance`, `login`, `repo_id`, `committed_date`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

-- ------------------------------------------------------
-- Table `github`.`repo_pull_requests`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`repo_pull_requests` ;

CREATE TABLE IF NOT EXISTS `github`.`repo_pull_requests` (
  `instance` VARCHAR(50) NOT NULL,
  `repo_id` INT(11) NULL DEFAULT NULL,
  `base_repo_id` INT(11) NULL DEFAULT NULL,
  `head_repo_id` INT(11) NULL DEFAULT NULL,
  `base_repo_brance_des` VARCHAR(200) NOT NULL,
  `head_repo_brance_des` VARCHAR(200) NOT NULL,
  `pull_request_user_id` INT(11) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`orgs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`orgs` ;

CREATE TABLE IF NOT EXISTS `github`.`orgs` (
  `instance` VARCHAR(50) NOT NULL,
  `org_name` VARCHAR(100) NOT NULL,
  `org_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`instance`, `org_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`orgs_admins`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`orgs_admins` ;

CREATE TABLE IF NOT EXISTS `github`.`orgs_admins` (
  `instance` VARCHAR(50) NOT NULL,
  `org_name` VARCHAR(100) NOT NULL,
  `admin_user_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`admin_user_id`, `instance`, `org_name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`orgs_members`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`orgs_members` ;

CREATE TABLE IF NOT EXISTS `github`.`orgs_members` (
  `instance` VARCHAR(50) NOT NULL,
  `org_name` VARCHAR(100) NOT NULL,
  `login` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`login`, `org_name`, `instance`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`orgs_teams`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`orgs_teams` ;

CREATE TABLE IF NOT EXISTS `github`.`orgs_teams` (
  `instance` VARCHAR(100) NOT NULL,
  `org_name` VARCHAR(100) NOT NULL,
  `team_name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`team_name`, `instance`, `org_name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`repos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`repos` ;

CREATE TABLE IF NOT EXISTS `github`.`repos` (
  `instance` VARCHAR(50) NOT NULL,
  `repo_id` INT(11) NULL DEFAULT NULL,
  `repo_name` VARCHAR(100) NOT NULL,
  `repo_full_name` VARCHAR(200) NOT NULL,
  `owner_name` VARCHAR(100) NOT NULL,
  `forked` BOOLEAN NULL DEFAULT NULL,
  `owner_type` CHAR(20) NULL DEFAULT NULL,
  `create_time` DATETIME NULL DEFAULT NULL,
  `visibility` VARCHAR(50) NULL DEFAULT NULL,
  `locked` BOOLEAN NULL DEFAULT NULL,
  `lock_reason` varchar(200) NULL DEFAULT NULL,
  `pushed_at` DATETIME NULL DEFAULT NULL,
  `parent_repo_name` VARCHAR(100),
  PRIMARY KEY (`instance`, `repo_full_name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`users` ;

CREATE TABLE IF NOT EXISTS `github`.`users` (
  `instance` VARCHAR(50) NOT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  `login` VARCHAR(100) NOT NULL,
  `primary_email` VARCHAR(200) NULL DEFAULT NULL,
  `suspended` BOOLEAN NULL DEFAULT NULL,
  `dormant` BOOLEAN NULL DEFAULT NULL,
  `site_admin` BOOLEAN NULL DEFAULT NULL,
  `last_active` VARCHAR(100) NULL DEFAULT NULL,
  `created_time` DATETIME NULL DEFAULT NULL,
  `ldap_accountType` CHAR(15) NULL DEFAULT NULL,
  `ldap_hpStatus` CHAR(20) NULL DEFAULT NULL,
  `ldap_hpeSpinCompany` CHAR(15) NULL DEFAULT NULL,
  `ldap_hpBusinessGroupCode` CHAR(10) NULL DEFAULT NULL,
  `ldap_uid` CHAR(50) NULL DEFAULT NULL,
  `last_web_session_time` DATETIME NULL DEFAULT NULL,
  `last_audit_log_entry_time` DATETIME NULL DEFAULT NULL,
  `last_dashboard_event_time` DATETIME NULL DEFAULT NULL,
  `last_repo_star_time` DATETIME NULL DEFAULT NULL,
  `last_repo_watch_time` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`instance`, `login`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`users_emails`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`users_emails` ;

CREATE TABLE IF NOT EXISTS `github`.`users_emails` (
  `instance` VARCHAR(50) NOT NULL,
  `login` VARCHAR(100) NOT NULL,
  `email` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`login`, `instance`, `email`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`users_ldap_emails`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`users_ldap_emails` ;

CREATE TABLE IF NOT EXISTS `github`.`users_ldap_emails` (
  `instance` VARCHAR(50) NOT NULL,
  `login` VARCHAR(100) NOT NULL,
  `email` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`email`, `login`, `instance`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`repos_admins`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`repos_admins` ;

CREATE TABLE IF NOT EXISTS `github`.`repos_admins` (
  `instance` VARCHAR(50) NOT NULL,
  `repo_full_name` VARCHAR(200) NOT NULL,
  `admin_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`admin_id`, `instance`, `repo_full_name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`repos_members`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`repos_members` ;

CREATE TABLE IF NOT EXISTS `github`.`repos_members` (
  `instance` VARCHAR(50) NOT NULL,
  `repo_full_name` VARCHAR(200) NOT NULL,
  `login` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`login`, `repo_full_name`, `instance`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `github`.`repos_teams`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `github`.`repos_teams` ;

CREATE TABLE IF NOT EXISTS `github`.`repos_teams` (
  `instance` VARCHAR(100) NOT NULL,
  `repo_full_name` VARCHAR(200) NOT NULL,
  `team_name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`team_name`, `instance`, `repo_full_name`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;