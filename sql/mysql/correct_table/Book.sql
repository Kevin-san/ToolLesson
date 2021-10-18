use alvin;
drop table IF EXISTS `Book`;
create table IF NOT EXISTS `Book`( -- 书的信息表
	`Id` INT AUTO_INCREMENT,
	`BookName` VARCHAR(100) NOT NULL, -- 书名
	`Description` VARCHAR(3000) NOT NULL, -- 介绍
	`Author` VARCHAR(100) NOT NULL, -- 作者
	`ImageContent` VARCHAR(300) NOT NULL DEFAULT '', -- 图片
	`CategoryId` INT UNSIGNED NOT NULL, -- 分类 (课程，小说)
	`MaxSectionId` INT NOT NULL, -- 最新
	`MaxSectionName` VARCHAR(300) NOT NULL DEFAULT '', -- 最新
	`UpdateTime` DATETIME NOT NULL, --更新时间
	`UpdateUser` VARCHAR(100) NOT NULL, --更新者
	`DeleteFlag` TINYINT NOT NULL DEFAULT 0, -- 删除状态
	`submission_user` VARCHAR(30), -- 上传人
	`submission_date` DATE, -- 上传时间
	PRIMARY KEY ( `Id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

delete from `Book`;
insert into `Book` values(512811,'Linux就该这么学','免费使用的类Unix操作系统','Linux','linux.png',11,20,'使用OpenLDAP部署目录服务',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512812,'Bash入门','Linux系统中默认的命令编程语言','Bash','bash.png',11,17,'常用命令大全',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512813,'Regex入门','一种对字符串操作的逻辑公式','正则表达式','regex.png',10,242994,'PHP',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512814,'软件设计模式','面向对象常用的设计模式','设计模式','design.png',11,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512815,'Docker入门','开源的应用容器引擎','Docker','docker.png',11,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512816,'Maven3入门','Java项目管理工具','Maven3','maven.png',11,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512817,'Python3.x入门','解释性,编译性,互动性和面向对象的脚本语言','Python3','python.png',11,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512818,'Java8入门','跨平台的面向对象的程序设计语言','Java8','java.png',11,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512819,'Perl5入门','高级,通用,直译式,动态的程序语言','Perl5','perl.png',11,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512820,'C++入门','前一代通用编程语言','C++','c++.png',11,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512821,'Go入门','谷歌推出的全新编程语言','Go','go.png',11,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512822,'标准SQL','结构化查询语言','SQL','SQL.png',12,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512823,'MySql/MariasDB','免费关系型数据库','MySql','mysql.png',12,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512824,'Oracle','收费关系型数据库','Oracle','oracle.png',12,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512825,'SqlServer','关系型数据库','SqlServer','sql-server.png',12,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512826,'Sybase','关系型数据库','Sybase','sybase.png',12,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512827,'SQLite','轻型数据库','SQLite','sqlite.png',12,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512828,'PostgreSQL','对象-关系型数据库','PostgreSQL','postgresql.png',12,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512829,'MongoDB','非关系型数据库','MongoDB','MongoDB.png',12,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512830,'Redis','高性能key-value缓存数据库','Redis','redis.png',12,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512831,'Html5','下一代HTML标准','Html','html.png',13,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512832,'Javascript','Web编程语言','Javascript','JavaScript.png',13,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512833,'Css','层叠样式表','CSS','CSS.png',13,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512834,'Android','基于Linux的移动操作系统','Android','android.png',14,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512835,'Kotlin','Android官方开发语言,类Java','Kotlin','kotlin.png',14,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512836,'Gradle','Android官方打包工具','Gradle','Gradle.png',14,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512837,'English','全球通用语言','English','english.jpg',17,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512838,'Japanese','动漫通用语言','Japanese','japanese.png',17,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512839,'组合数学','用算法处理离散对象','Combinatorics','math.png',15,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512840,'线性代数','解决线性关系问题','LinearAlgebra','line_math.png',15,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512841,'概率统计','统计计数调查','ProbabilityAxioms','math_rate.png',15,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512842,'微积分','微分学和积分学','Calculus','math_score.png',15,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512843,'数论','研究整数的性质','NumberTheory','math_theory.png',15,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512844,'极客技术','保护系统不被病毒攻击','GeekTechnology','Geek-2.png',16,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512845,'机器学习','使用计算机提高学习效率','MachineLearning','machine_l.png',16,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512846,'深度学习','模式分析方法','DeepLearning','deep_learning.png',16,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512847,'数据挖掘','通过算法搜索隐藏信息','DataMining','data_search.png',16,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512848,'网络爬虫','按一定规则爬取网站信息','WebCrawler','web_crawler.png',16,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512849,'语音合成','人造语音','SpeechSynthesis','speech_synthesis.png',16,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512850,'语音识别','识别语音语言的技术','VoiceRecognition','voice_recognition.png',16,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512851,'区块链','去中心化数据块','BlockChain','block_chain.png',16,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512852,'3D建模','制作3D模型','3DModel','3D_model.png',16,0,'',now(),'alvin',0,'alvin',curdate());
insert into `Book` values(512853,'Unity3D','游戏制作引擎','Unity3D','Unity3D.png',16,0,'',now(),'alvin',0,'alvin',curdate());

insert into Book select Id,Name,'','','',SourceId + 100,0,'',now(),'alvin',DeleteFlag,submission_user,submission_date FROM spideritem WHERE SourceId <=8;
update book b INNER JOIN spiderproperty sp ON b.Id=sp.ItemId AND sp.PropertyKey='作者' set b.Author = sp.PropertyValue;
update book b INNER JOIN spiderproperty sp ON b.Id=sp.ItemId AND sp.PropertyKey='简介' set b.Description = sp.PropertyValue;
update book b INNER JOIN spiderproperty sp ON b.Id=sp.ItemId AND sp.PropertyKey='图片' set b.ImageContent = case when sp.PropertyValue = '' then 'novel_bg.jpg' else sp.PropertyValue end;
update book b INNER JOIN spiderproperty sp ON b.Id=sp.ItemId AND sp.PropertyKey='最新' set b.MaxSectionId = sp.PropertyValue , b.MaxSectionName = sp.PropertyBigVal;