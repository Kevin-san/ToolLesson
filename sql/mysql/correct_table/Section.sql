use alvin;
drop table IF EXISTS `Section`;
create table IF NOT EXISTS `Section`( -- 书的大章节表
	`Id` INT AUTO_INCREMENT,
	`BookId` INT NOT NULL, -- 课程id
	`OrderNo` INT NOT NULL, -- 第几章
	`SectionNo` INT NOT NULL DEFAULT 0, -- 第几节
	`ChapterName` VARCHAR(100) character set utf8 NOT NULL, -- 章节名
	`Content` TEXT character set utf8 NOT NULL, -- 章节内容
	`UpdateTime` DATETIME NOT NULL, --更新时间
	`UpdateUser` VARCHAR(100) NOT NULL, --更新者
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
insert into Section(BookId,OrderNo,SectionNo,ChapterName,Content,UpdateTime,UpdateUser,DeleteFlag,submission_user,submission_date) SELECT cp.BookLesson_Id,cp.ChapterNo,0,cp.ChapterName,group_concat(case 
when ct.ElementTag = 'h1' then CONCAT('# ',ct.Text)
when ct.ElementTag = 'h2' then CONCAT('## ',ct.Text)
when ct.ElementTag = 'h3' then CONCAT('### ',ct.Text)
when ct.ElementTag = 'h4' then CONCAT('#### ',ct.Text)
when ct.ElementTag = 'h5' then CONCAT('##### ',ct.Text)
when ct.ElementTag = 'image' then CONCAT('![](',replace(ct.Text,'/static','') ,')')
when ct.ElementTag = 'em' then CONCAT('***',ct.Text,'***')
when ct.ElementTag = 'i' then CONCAT('*',ct.Text,'*')
when ct.ElementTag = 'line' then '---'
when ct.ElementTag = 'ol' then replace(ct.Text,'\r\n','\r\n- ')
when ct.ElementTag = 'ul' then replace(ct.Text,'\r\n','\r\n- ')
when ct.ElementTag = 'p' then concat(ct.Text,'\r\n')
when ct.ElementTag = 'pre' then CONCAT('```',ct.Text,'```')
when ct.ElementTag = 'strong' then CONCAT('**',ct.Text,'**')
when ct.ElementTag = 'table' then replace(ct.Text,'	','|') ELSE '' END SEPARATOR '\r\n'),now(),'alvin',
0,'alvin',CURDATE()
  FROM content ct, Chapter cp WHERE ct.Chapter_Id = cp.Id GROUP BY  cp.Id, cp.ChapterNo,cp.ChapterName,cp.BookLesson_Id;
update Section set BookId = BookId +512810;

update Section set Content = replace(Content,'BOLD[','**');
update Section set Content = replace(Content,']BOLD','**');
update Section set Content = replace(Content,'BLUE_BG[','***');
update Section set Content = replace(Content,']BLUE_BG','***');

insert into Section(BookId,OrderNo,SectionNo,ChapterName,Content,UpdateTime,UpdateUser,DeleteFlag,submission_user,submission_date) SELECT sp.Id,si.Id,sp.OrderId,0,sp.PropertyValue,sp.PropertyBigVal,now(),'alvin',0,'alvin',CURDATE() FROM spiderproperty sp,spideritem si WHERE si.Id = sp.ItemId AND sp.PropertyKey = '章节' AND si.DeleteFlag IN ( 1,2) and si.SourceId=1
update Section set Content = replace(Content,'\n\n','')
update Section set Content = replace(Content,'\n','\r\n\r\n')
update Section set Content = replace(Content,'铅笔小说','')
update Section set Content = replace(Content,'a1bm();','')
