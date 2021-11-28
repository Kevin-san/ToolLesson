use alvin;
drop table IF EXISTS `SpiderTriggerResult`;
create table IF NOT EXISTS `SpiderTriggerResult`( -- 爬虫表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`TriggerId` INT NOT NULL,
	`CategoryFather` INT NOT NULL,
	`CategoryId` INT NOT NULL,
	`CoverImg` VARCHAR(1000) NOT NULL,
	`Title` VARCHAR(1000) NOT NULL,
	`VUrl` VARCHAR(1000) NOT NULL,
	`DownloadFolder` VARCHAR(1000) NOT NULL,
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`CreateTime` DATETIME NOT NULL DEFAULT NOW(), --创建时间
	`UpdateTime` DATETIME NOT NULL DEFAULT NOW(), --更新时间
	`submission_user` VARCHAR(30) DEFAULT 'alvin', -- 上传人
	`submission_date` DATE DEFAULT curdate(), -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into spidertriggerresult(TriggerId,CategoryFather,CategoryId,CoverImg,Title,VUrl,DownloadFolder) values()

UPDATE spidertriggerresult SET VUrl= REPLACE(VUrl,'163.34885.xyz','yy.34885.xyz') WHERE CategoryId >= 3009
UPDATE spidertriggerresult SET VUrl= REPLACE(VUrl,'163.34885.xyz','163.34885.xyz/changpian') WHERE CategoryId < 3009