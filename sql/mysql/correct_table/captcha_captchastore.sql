use alvin;

drop table IF EXISTS `captcha_captchastore`;

create table IF NOT EXISTS `captcha_captchastore`(
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`challenge` CHAR(32) NOT NULL,
	`response` CHAR(32) NOT NULL,
	`hashkey` CHAR(40) UNIQUE NOT NULL,
	`expiration` DATETIME,
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
