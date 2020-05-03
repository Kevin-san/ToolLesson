
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','index','Shell 简介','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','param','Shell 变量','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','env','Shell 环境变量','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','argvs','Shell 传递参数','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','str','Shell 字符串','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','comment','Shell 注释','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','escapechar','Shell 转义符','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','operator','Shell 运算符','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','array','Shell 数组','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','hash','Shell 哈希','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','test','Shell test命令','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','func','Shell 函数','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','forever','Shell 流程控制','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','output','Shell 输入/输出重定向','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','include','Shell 文件包含','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','vim','Shell vi/vim','alvin');
insert into LessonMenu(MenuType,Href,Text,submission_user) values('bash','cmds','Shell 常用命令大全','alvin');

insert into LessonDetails(ParentKey,Type,OrderIndex,Level,Text,submission_user) values('bash-index','h1',1,1,'强大好用的Shell(Bash4)','alvin');
insert into LessonDetails(ParentKey,Type,OrderIndex,Level,Text,submission_user) values('bash-index','p',2,1,'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通常来讲，计算机硬件是由运算器、控制器、存储器、输入/输出设备等共同组成的，而让各种硬件设备各司其职且又能协同运行的就是系统内核。Linux系统的内核负责完成对硬件资源的分配、调度等管理任务。由此可见，系统内核对计算机的正常运行来讲是太重要了，因此一般不建议直接去编辑内核中的参数，而是让用户通过基于系统调用接口开发出的程序或服务来管理计算机，以满足日常工作的需要。<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;必须肯定的是，Linux系统中有些图形化工具(比如逻辑卷管理器[Logical Volume Manager,LVM])确实非常好用，极大地降低了运维人员操作出错的概率，值得称赞。但是，很多图形化工具其实是调用了脚本来完成相应的工作，往往只是为了完成某种工作来设计的，缺乏Linux命令原有的灵活性及可控性。再者，图形化工具相较于Linux命令行界面会更加消耗系统资源，因此经验丰富的运维人员甚至都不会给Linux系统安装图形界面，需要开始运维工作时直接通过命令行模式远程连接过去，不得不说这样做确实挺高效的。<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Shell就是这样的一个命令行工具。Shell(也称终端或壳)充当的是人与内核(硬件)之间的翻译官，用户把一些命令\'告诉终端\'，它就会调用相应的程序服务去完成某些工作。','alvin');
insert into LessonDetails(ParentKey,Type,OrderIndex,Level,Text,ParentFlag,submission_user) valuesvalues('bash-index','pre',3,1,'',1,'alvin');
insert into LessonDetails(ParentKey,Type,OrderIndex,Level,Text,submission_user) values('bash-index','strong',1,2,'<em>通过上下方向键来调取过往执行过的Linux命令；</em>','alvin');
insert into LessonDetails(ParentKey,Type,OrderIndex,Level,Text,submission_user) values('bash-index','strong',2,2,'<em>命令或参数仅需输入前几位就可以用Tab键补全；</em>','alvin');
insert into LessonDetails(ParentKey,Type,OrderIndex,Level,Text,submission_user) values('bash-index','strong',3,2,'<em>具有强大的批处理脚本；</em>','alvin');
insert into LessonDetails(ParentKey,Type,OrderIndex,Level,Text,submission_user) values('bash-index','strong',4,2,'<em>具有实用的环境变量功能；</em>','alvin');