use alvin;
drop table IF EXISTS `SpiderTrigger`;
create table IF NOT EXISTS `SpiderTrigger`( -- 爬虫触发表
	`Id` INT UNSIGNED AUTO_INCREMENT,
	`HomeUrl` VARCHAR(1000) NOT NULL DEFAULT '', -- 网址
	`RequestUrl` VARCHAR(1000) NOT NULL DEFAULT '', -- 网址
	`TriggerCategoryId` INT NOT NULL, -- 分类
	`TriggerParams` VARCHAR(1000) NOT NULL DEFAULT '', -- 参数
	`TriggerCategoryKey` VARCHAR(1000) NOT NULL DEFAULT '', -- 参数
	`MapUrl` VARCHAR(1000) NOT NULL, -- 网址
	`DownloadFolder` VARCHAR(1000) NOT NULL, -- 下载目录
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`CreateTime` DATETIME NOT NULL, --创建时间
	`UpdateTime` DATETIME NOT NULL, --更新时间
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into SpiderTrigger values(1,'https://4hqg.com/web/','https://4hqg.com/web/abcdefg.ashx',1010,'action=getvideos,pageindex=1,pagesize=20000,tags=全部','vtype','https://163.34885.xyz','I:/Hider/Video',0,now(),now(),'alvin',curdate())

