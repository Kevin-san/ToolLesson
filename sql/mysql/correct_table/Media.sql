use alvin;
drop table IF EXISTS `Media`;
create table IF NOT EXISTS `Media`( -- 音视频的信息表
	`Id` INT AUTO_INCREMENT,
	`MediaName` VARCHAR(1000) NOT NULL, -- 名字
	`ParentDir` VARCHAR(100) NOT NULL,-- 父目录
	`Content` VARCHAR(3000) NOT NULL, -- 内容
	`Authors` VARCHAR(300) NOT NULL, -- 作者
	`ImageContent` VARCHAR(100) NOT NULL DEFAULT '', -- 图片
	`CategoryId` INT UNSIGNED NOT NULL, -- 分类 (视频，音频)
	`TotalTime` INT NOT NULL, -- 时长 s 网页显示 按 min / hour
	`TotalSize` BIGINT NOT NULL, -- 大小 b 网页显示按 Mb / Gb
	`UpdateTime` DATETIME NOT NULL, --更新时间
	`UpdateUser` VARCHAR(100) NOT NULL, --更新者
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into Media SELECT Id,Name,CONCAT('/img/美女/',Name,''),'','',CONCAT('/img/美女/',Name,CONCAT('/',Name,'_0.jpg')),SourceId+200,0,0,now(),'alvin',0,'alvin',curdate() FROM spideritem WHERE SourceId >=15 AND DeleteFlag = 2;
update spideritem set DeleteFlag = -2 where SourceId >=15 AND DeleteFlag = 2;