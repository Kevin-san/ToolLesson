use alvin;
drop table IF EXISTS `MediaSection`;
create table IF NOT EXISTS `MediaSection`( -- 音视频的大章节表
	`Id` INT AUTO_INCREMENT,
	`MediaId` INT NOT NULL, -- Media id
	`OrderNo` INT NOT NULL DEFAULT 0, -- 第几章
	`SectionNo` INT NOT NULL DEFAULT 0, -- 第几节
	`Preffix` VARCHAR(10) NOT NULL, -- 后缀
	`Time` INT NOT NULL, -- 时长 s 网页显示 按 min / hour
	`Size` BIGINT NOT NULL, -- 大小 b 网页显示按 Mb / Gb
	`UpdateTime` DATETIME NOT NULL, --更新时间
	`UpdateUser` VARCHAR(100) NOT NULL, --更新者
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE MediaSection ADD INDEX  `media_section_index`(`MediaId`,`OrderNo`);
insert into MediaSection(MediaId,OrderNo,SectionNo,Preffix,Time,Size,UpdateTime,UpdateUser,DeleteFlag,submission_user,submission_date) SELECT ItemId,OrderId,0,'jpg',0,0,now(),'alvin',0,'alvin',curdate() FROM SpiderProperty WHERE PropertyKey = '序号' and DeleteFlag = 2;
update SpiderProperty set DeleteFlag  = -2 where DeleteFlag = 2 and PropertyKey = '序号';