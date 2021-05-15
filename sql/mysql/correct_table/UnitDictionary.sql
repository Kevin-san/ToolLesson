use alvin;
drop table IF EXISTS `UnitDictionary`;
create table IF NOT EXISTS `UnitDictionary`( -- 单位字典表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`ConversionType` VARCHAR(100) NOT NULL, -- 换算种类
	`UnitFromKey` VARCHAR(100) NOT NULL, -- 因单位
	`UnitToKey` VARCHAR(100) NOT NULL, -- 果单位
	`UnitValue` FLOAT NOT NULL, -- 单位值
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;