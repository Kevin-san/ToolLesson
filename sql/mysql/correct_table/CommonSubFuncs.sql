use alvin;
drop table IF EXISTS `CommonSubFuncs`;
create table IF NOT EXISTS `CommonSubFuncs`( -- 功能的信息表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`FunctionName` VARCHAR(100) NOT NULL, -- 功能名
	`FunctionHref` VARCHAR(100) NOT NULL, -- 功能链接
	`FunctionDesc` VARCHAR(2000),
	`CommonMainType_Id` INT NOT NULL, -- 功能分类
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;