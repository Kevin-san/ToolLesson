use alvin;
drop table IF EXISTS `LanguageDictionary`;
create table IF NOT EXISTS `LanguageDictionary`(
	`LanguageValue` VARCHAR(200) NOT NULL,
	`LanguageTypeId` VARCHAR(200) NOT NULL,
	`CatergoryTypeId` VARCHAR(20) NOT NULL,
	`LanguageSingleType` VARCHAR(200) NOT NULL,
	`ChineseContent` VARCHAR(200),
	`SamplePattern1` VARCHAR(200),
	`SamplePattern2` VARCHAR(200),
	`SamplePattern3` VARCHAR(200),
	`SamplePattern4` VARCHAR(200),
	`SamplePattern5` VARCHAR(200),
	`SamplePattern6` VARCHAR(200),
	`SamplePattern7` VARCHAR(200),
	`SamplePattern8` VARCHAR(200),
	`SamplePattern9` VARCHAR(200),
	`SamplePattern10` VARCHAR(200),
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0,
	`submission_user` VARCHAR(30),
	`submission_date` DATE,
	PRIMARY KEY ( `CategoryId` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
