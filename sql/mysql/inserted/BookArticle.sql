
insert into BookArticle values(1,1,'/bash/index','h2','强大好用的Shell(Bash4)',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(2,2,'/bash/index','p','        通常来讲，计算机硬件是由运算器、控制器、存储器、输入/输出设备等共同组成的，而让各种硬件设备各司其职且又能协同运行的就是系统内核。Linux系统的内核负责完成对硬件资源的分配、调度等管理任务。由此可见，系统内核对计算机的正常运行来讲是太重要了，因此一般不建议直接去编辑内核中的参数，而是让用户通过基于系统调用接口开发出的程序或服务来管理计算机，以满足日常工作的需要。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(3,3,'/bash/index','p','        必须肯定的是，Linux系统中有些图形化工具(比如逻辑卷管理器[Logical Volume Manager,LVM])确实非常好用，极大地降低了运维人员操作出错的概率，值得称赞。但是，很多图形化工具其实是调用了脚本来完成相应的工作，往往只是为了完成某种工作来设计的，缺乏Linux命令原有的灵活性及可控性。再者，图形化工具相较于Linux命令行界面会更加消耗系统资源，因此经验丰富的运维人员甚至都不会给Linux系统安装图形界面，需要开始运维工作时直接通过命令行模式远程连接过去，不得不说这样做确实挺高效的。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(4,4,'/bash/index','p','        Shell就是这样的一个命令行工具。Shell(也称终端或壳)充当的是人与内核(硬件)之间的翻译官，用户把一些命令\'告诉终端\'，它就会调用相应的程序服务去完成某些工作。现在包括红帽系统在内的许多主流Linux系统默认使用的终端是Bash(Bourne-Again Shell)解释器。主流Linux系统选择Bash解释器作为命令行终端主要有以下4项优势:',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(5,5,'/bash/index','ul','通过上下方向键来调取过往执行过的Linux命令；
命令或参数仅需输入前几位就可以用Tab键补全；
具有强大的批处理脚本；
具有实用的环境变量功能；',null,null,null,null,null,null,null,0,'alvin','1900-01-01');

insert into BookArticle values(6,1,'/bash/param','p','变量是计算机系统用于保存可变值的数据类型。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(7,2,'/bash/param','p','运行shell时，会同时存在三种变量：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(8,3,'/bash/param','ol','局部变量 : 局部变量在脚本或命令中定义，仅在当前shell实例中有效，其他shell启动的程序不能访问局部变量。
环境变量 : 所有的程序，包括shell启动的程序，都能访问环境变量，有些程序需要环境变量来保证其正常运行。必要的时候shell脚本也可以定义环境变量。
shell变量 : shell变量是由shell程序设置的特殊变量。shell变量中有一部分是环境变量，有一部分是局部变量，这些变量保证了shell的正常运行。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(9,4,'/bash/param','p','定义变量时，变量名不加美元符号（$，PHP语言中变量需要），如：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(10,5,'/bash/param','pre','your_name="test.com"',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(11,6,'/bash/param','p','注意，变量名和等号之间不能有空格，这可能和你熟悉的所有编程语言都不一样。同时，变量名的命名须遵循如下规则：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(12,7,'/bash/param','ul','命名只能使用英文字母，数字和下划线，首个字符不能以数字开头。
中间不能有空格，可以使用下划线（_）。
不能使用标点符号。
不能使用bash里的关键字（可用help命令查看保留关键字）。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(13,8,'/bash/param','p','有效的 Shell 变量名示例如下：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(14,9,'/bash/param','pre','RUNOOB
LD_LIBRARY_PATH
_var
var2',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(15,10,'/bash/param','p','无效的变量命名：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(16,11,'/bash/param','pre','?var=123
user*name=runoob',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(17,12,'/bash/param','p','除了显式地直接赋值，还可以用语句给变量赋值，如：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(18,13,'/bash/param','pre','for file in `ls /etc`
或
for file in $(ls /etc)',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(19,14,'/bash/param','p','以上语句将 /etc 下目录的文件名循环出来。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(20,15,'/bash/param','hr','',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(21,16,'/bash/param','h3','使用变量',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(22,17,'/bash/param','p','使用一个定义过的变量，只要在变量名前面加美元符号即可，如：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(23,18,'/bash/param','pre','your_name="qinjx"
echo $your_name
echo ${your_name}',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(24,19,'/bash/param','p','变量名外面的花括号是可选的，加不加都行，加花括号是为了帮助解释器识别变量的边界，比如下面这种情况：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(25,20,'/bash/param','pre','for skill in Ada Coffe Action Java; do
    echo "I am good at ${skill}Script"
done',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(26,21,'/bash/param','p','如果不给skill变量加花括号，写成echo "I am good at $skillScript"，解释器就会把$skillScript当成一个变量（其值为空），代码执行结果就不是我们期望的样子了。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(27,22,'/bash/param','p','推荐给所有变量加上花括号，这是个好的编程习惯。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(28,23,'/bash/param','p','已定义的变量，可以被重新定义，如：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(29,24,'/bash/param','pre','your_name="tom"
echo $your_name
your_name="alibaba"
echo $your_name',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(30,25,'/bash/param','p','这样写是合法的，但注意，第二次赋值的时候不能写$your_name="alibaba"，使用变量的时候才加美元符（$）。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(31,26,'/bash/param','hr','',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(32,27,'/bash/param','h3','只读变量',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(33,28,'/bash/param','p','使用 readonly 命令可以将变量定义为只读变量，只读变量的值不能被改变。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(34,29,'/bash/param','p','下面的例子尝试更改只读变量，结果报错：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(35,30,'/bash/param','pre','#!/bin/bash

myUrl="http://www.google.com"
readonly myUrl
myUrl="http://www.runoob.com"',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(36,31,'/bash/param','p','运行脚本，结果如下：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(37,32,'/bash/param','pre','/bin/sh: NAME: This variable is read only.',null,null,null,null,null,null,null,0,'alvin','1900-01-01');

insert into BookArticle values(38,1,'/bash/env','p','环境变量是用来定义系统运行环境的一些参数，并允许将数据存储在内存中。比如每个用户不同的家目录、邮件存放位置等。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(39,2,'/bash/env','p','设置全局环境变量的命令格式：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(40,3,'/bash/env','p','export 变量名=值      # 注意在设置环境变量的时候，[变量=值]之间不能添加空格，要不然shell会把它当做一个单独的命令执行 

或者

变量名=值
export 变量名        # 注意export 命令中不需要$符号 ',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(41,4,'/bash/env','p','为了通过环境变量帮助Linux系统构建起能够为用户提供服务的工作运行环境，需要数百个变量协同工作才能完成。您当然没有必要去把每一个变量都看一遍，而应该在最宝贵的书籍中为读者精讲最重要的内容。为了更好地帮助大家理解变量的作用，刘遄老师给大家举个例子。前文中曾经讲到，在Linux系统中一切都是文件，Linux命令也不例外。那么，在用户执行了一条命令之后，Linux系统中到底发生了什么事情呢？简单来说，命令在Linux中的执行分为4个步骤。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(42,5,'/bash/env','ol','判断用户是否以绝对路径或相对路径的方式输入命令（如/bin/ls），如果是的话则直接执行。
Linux系统检查用户输入的命令是否为“别名命令”，即用一个自定义的命令名称来替换原本的命令名称。可以用alias命令来创建一个属于自己的命令别名，格式为“alias别名=命令”。若要取消一个命令别名，则是用unalias命令，格式为“unalias别名”。我们之前在使用rm命令删除文件时，Linux系统都会要求我们再确认是否执行删除操作，其实这就是Linux系统为了防止用户误删除文件而特意设置的rm别名命令，接下来我们把它取消掉：
Bash解释器判断用户输入的是内部命令还是外部命令。内部命令是解释器内部的指令，会被直接执行；而用户在绝大部分时间输入的是外部命令，这些命令交由步骤4继续处理。可以使用“type命令名称”来判断用户输入的命令是内部命令还是外部命令。
系统在多个路径中查找用户输入的命令文件，而定义这些路径的变量叫作PATH，可以简单地把它理解成是“解释器的小助手”，作用是告诉Bash解释器待执行的命令可能存放的位置，然后Bash解释器就会乖乖地在这些位置中逐个查找。PATH是由多个路径值组成的变量，每个路径值之间用冒号间隔，对这些路径的增加和删除操作将影响到Bash解释器对Linux命令的查找。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(43,6,'/bash/env','pre','[root@linuxprobe ~]# ls 
anaconda-ks.cfg Documents initial-setup-ks.cfg Pictures Templates Desktop Downloads Music Public Videos 
[root@linuxprobe ~]# rm anaconda-ks.cfg 
rm:remove regular file ‘anaconda-ks.cfg’? y 
[root@linuxprobe ~]# alias rm 
alias rm=\'rm -i\'
[root@linuxprobe ~]# unalias rm 
[root@linuxprobe ~]# rm initial-setup-ks.cfg 
[root@linuxprobe ~]#',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(44,7,'/bash/env','pre','[root@linuxprobe ~]# echo $PATH 
/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin 
[root@linuxprobe ~]# PATH=$PATH:/root/bin 
[root@linuxprobe ~]# echo $PATH 
/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:/root/bin',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(45,8,'/bash/env','hr','',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(46,9,'/bash/env','h3','PATH全局环境变量',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(47,10,'/bash/env','p','修改PATH环境变量：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(48,11,'/bash/env','pre','PATH=$PATH:新加目录',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(49,12,'/bash/env','strong','这里有比较经典的问题：“为什么不能将当前目录（.）添加到PATH中呢?”原因是，尽管可以将当前目录（.）添加到PATH变量中，从而在某些情况下可以让用户免去输入命令所在路径的麻烦。但是，如果黑客在比较常用的公共目录/tmp中存放了一个与ls或cd命令同名的木马文件，而用户又恰巧在公共目录中执行了这些命令，那么就极有可能中招了。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(50,13,'/bash/env','p','所以，作为一名态度谨慎、有经验的运维人员，在接手了一台Linux系统后一定会在执行命令前先检查PATH变量中是否有可疑的目录，另外读者从前面的PATH变量示例中是否也感觉到环境变量特别有用呢。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(51,14,'/bash/env','hr','',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(52,15,'/bash/env','h3','Linux 系统中最重要的10个环境变量',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(53,16,'/bash/env','table','变量名称#^#作用
HOME#^#用户的主目录（即家目录）
SHELL#^#用户在使用的Shell解释器名称
HISTSIZE#^#输出的历史命令记录条数
HISTFILESIZE#^#保存的历史命令记录条数
MAIL#^#邮件保存路径
LANG#^#系统语言、语系名称
RANDOM#^#生成一个随机数字
PS1#^#Bash解释器的提示符
PATH#^#定义解释器搜索用户执行命令的路径
EDITOR#^#用户默认的文本编辑器',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(54,17,'/bash/env','p','Linux作为一个多用户多任务的操作系统，能够为每个用户提供独立的、合适的工作运行环境，因此，一个相同的变量会因为用户身份的不同而具有不同的值。例如，我们使用下述命令来查看HOME变量在不同用户身份下都有哪些值（su是用于切换用户身份的命令，将在下文跟大家见面）：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(55,18,'/bash/env','pre','[root@linuxprobe ~]# echo $HOME 
/root 
[root@linuxprobe ~]# su - linuxprobe 
Last login: Fri Feb 27 19:49:57 CST 2017 on pts/0
[linuxprobe@linuxprobe ~]$ echo $HOME 
/home/linuxprobe',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(56,19,'/bash/env','hr','',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(57,20,'/bash/env','h2','环境变量分为：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(58,21,'/bash/env','ul','全局环境变量
本地环境变量',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(59,22,'/bash/env','hr','',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(60,23,'/bash/env','h3','全局环境变量',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(61,24,'/bash/env','p','在当前shell和子shell都可见，可以用printenv和env命令查看全局环境变量，大写表示是系统环境变量，小写表示是普通用户的环境变量。这是bash shell的一个标准约定，不是必须的，因此在设置新的环境变量的时候我们用小写就行了，用于区分个人和系统环境变量。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(62,25,'/bash/env','p','如下例：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(63,26,'/bash/env','pre','[root@CentOS6 ~]# printenv
或 
[root@CentOS6 ~]# env
TERM=linux
SHELL=/bin/bash
HISTSIZE=1000
SSH_CLIENT=172.18.251.124 8132 22
QTDIR=/usr/lib64/qt-3.3
QTINC=/usr/lib64/qt-3.3/include
SSH_TTY=/dev/pts/4
name=hello        # 自己定义的环境变量
USER=root
LS_COLORS=...
MAIL=/var/spool/mail/root
PATH=/usr/lib64/qt-3.3/bin:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
PWD=/root
LANG=en_US.UTF-8
PS1=[\[\e[33m\]\u@\[\e[34m\]\h \[\e[m\]\W]\$ \[\e[m\]
SSH_ASKPASS=/usr/libexec/openssh/gnome-ssh-askpass
HISTCONTROL=ignoredups
PS2=\[\e[34m\]> \[\e[m\]
SHLVL=1
HOME=/root
LOGNAME=root
QTLIB=/usr/lib64/qt-3.3/lib
CVS_RSH=ssh
SSH_CONNECTION=172.18.251.124 8132 172.18.250.183 22
LESSOPEN=||/usr/bin/lesspipe.sh %s
DISPLAY=localhost:12.0
G_BROKEN_FILENAMES=1
_=/usr/bin/printenv',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(64,27,'/bash/env','p','大部分变量都是在登录主shell时设置的',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(65,28,'/bash/env','hr','',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(66,29,'/bash/env','h3','本地环境变量',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(67,30,'/bash/env','p','只在当前shell中可见，可以通过set命令查看，不过set命令查看的是所有环境变量（全局和本地）',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(68,31,'/bash/env','hr','',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(69,32,'/bash/env','h3','删除变量',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(70,33,'/bash/env','p','使用 unset 命令可以删除变量。语法：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(71,34,'/bash/env','pre','unset variable_name',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(72,35,'/bash/env','ul','变量被删除后不能再次使用。unset 命令不能删除只读变量。
如果在子shell下删除全局环境变量，删除操作只对子shell有效，如果回到父shell下，该全局变量还能引用',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(73,36,'/bash/env','p','实例',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(74,37,'/bash/env','pre','#!/bin/sh
myUrl="http://www.runoob.com"
unset myUrl
echo $myUrl',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(75,38,'/bash/env','p','以上实例执行将没有任何输出。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(76,39,'/bash/env','hr','',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(77,40,'/bash/env','h3','设置系统环境变量的相关文件',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(78,41,'/bash/env','p','系统环境变量是在shell启动过程中执行相关的文件定义的。这些文件被称为shell启动文件。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(79,42,'/bash/env','p','shell分为四种shell:',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(80,43,'/bash/env','ul','登录式shell
非登录式shell
交互式shell
非交互式shell',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(81,44,'/bash/env','strong','我们在设置系统环境变量的时候，我们要区分不同shell的区别，（登录/非登录和交互/非交互只是划分的标准不一样）只有弄清除了不同模式的shell才能正确修改相应的shell启动文件以至于能够正确设置系统环境变量。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(82,45,'/bash/env','h4','1、登录式shell',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(83,46,'/bash/env','p','登录式shell是用户需要输入用户名和密码的shell，该模式的shell启动过程中会依次执行下列文件:',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(84,47,'/bash/env','pre','/etc/profile    # 登录bash shell的默认主启动文件。任何用户登录shell都会执行此启动文件。不建议修改
~/.bash_profile
~/.bash_login
~/.profile      # 上诉这三个$HOME启动文件是定义对应用户的环境变量。不同linux发行版使用的文件不同  ',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(85,48,'/bash/env','p','/etc/profile中的命令和脚本不是我们现在关注的，我们主要来看看export那一行，因此我们可以知道该文件是设置系统全局环境变量/etc/profile另一个重要的功能就是能够重复执行/etc/profile.d/目录下的文件（大多是.sh和.csh结尾的文件），这些文件大概是特定应用程序的启动文件，能够设置相关应用程序的环境变量，例如/etc/profile.d/lang.*sh就是用来设置LANG环境变量的。$HOME启动文件，我的系统用的~/.bash_profile,这些文件都是以.开头，代表了都是隐藏文件，同时是针对特定用户的，因此用户可以修改该文件。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(86,49,'/bash/env','pre','[root@CentOS6 ~]# cat /etc/profile
# /etc/profile

# System wide environment and startup programs, for login setup
# Functions and aliases go in /etc/bashrc

# It\'s NOT a good idea to change this file unless you know what you
# are doing. It\'s much better to create a custom.sh shell script in
# /etc/profile.d/ to make custom changes to your environment, as this
# will prevent the need for merging in future updates.
...

export PATH USER LOGNAME MAIL HOSTNAME HISTSIZE HISTCONTROL

...

for i in /etc/profile.d/*.sh
do
    if [ -r "$i" ]
    then
        if [ "${-#*i}" != "$-" ]
        then
            . "$i"
        else
            . "$i" >/dev/null 2>&1
        fi
    fi
done

unset i
unset -f pathmunge
[root@CentOS6 ~]#',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(87,50,'/bash/env','p','我们看下~/.bash_profile文件下的内容定义PATH的那一行。$HOME文件定义特定用户的PATH=$PATH:$HOME/bin，代表我们可以将可执行文件放在$HOME/bin目录下。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(88,51,'/bash/env','pre','[root@CentOS6 profile.d]# cat ~/.bash_profile 
# .bash_profile
# Get the aliases and functions
if [ -f ~/.bashrc ]
then
. ~/.bashrc
fi
# User specific environment and startup programs
PATH=$PATH:$HOME/bin
export PATH',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(89,52,'/bash/env','h4','2、非登录式shell',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(90,53,'/bash/env','p','登录式shell是需要输入用户名、密码登录的shell，而非登录式shell则是不需要的，例如直接在命令行输入bash、在图形化界面点击open in terminal开启命令行终端等都是非登录式shell。 另外，对于退出shell的命令exit和logout的区别，<strong>exit命令可以退出登录式shell和非登录式shell，logout只能退出登录式shell。</strong>',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(91,54,'/bash/env','pre','[root@CentOS6 bin]# bash
[root@CentOS6 bin]# logout
bash: lougout: not login shell: use `exit`
[root@CentOS6 bin]# exit
exit',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(92,55,'/bash/env','p','我们可以通过$0变量值来查看是登录式shell还是非登录式shell，登录式shell会在前面显示‘-’非登录式shell则没有',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(93,56,'/bash/env','pre','[root@CentOS6 bin]# echo $0  # 当前为登录式shell
-bash
[root@CentOS6 bin]# bash
[root@CentOS6 bin]# echo $0  # 当前为非登录式shell
bash
[root@CentOS6 bin]# ',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(94,57,'/bash/env','p','在非登录式shell的启动过程中，由于不需要重复的登录shell，所以非登录shell只需要执行下列文件即可，$HOME/.bashrc # 下面的内容说明',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(95,58,'/bash/env','pre','[root@CentOS6 ~]# cat ~/.bashrc 
# .bashrc
# User specific aliases and functions
alias rm=\'rm -i\'
alias cp=\'cp -i\'
alias mv=\'mv -i\'
alias cdnet=\'cd /etc/sysconfig/network-scripts/\'
alias ping=\'ping -c 4\'
# Source global definitions
if [ -f /etc/bashrc ]
then
. /etc/bashrc
fi',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(96,59,'/bash/env','p','该$HOME/.bashrc可以定义用户自定义的别名和函数，另外还有引用公共/etc/bashrc下的变量，我们来看看/etc/bashrc文件内容',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(97,60,'/bash/env','pre','[root@CentOS6 ~]# cat /etc/bashrc 
# /etc/bashrc

# System wide functions and aliases
# Environment stuff goes in /etc/profile

# It\'s NOT a good idea to change this file unless you know what you
# are doing. It\'s much better to create a custom.sh shell script in
# /etc/profile.d/ to make custom changes to your environment, as this
# will prevent the need for merging in future updates.

# are we an interactive shell?
...

    # Only display echos from profile.d scripts if we are no login shell
    # and interactive - otherwise just process them to set envvars
    for i in /etc/profile.d/*.sh
    do
        if [ -r "$i" ]
        then
            if [ "$PS1" ]
            then
                . "$i"
            else
                . "$i" >/dev/null 2>&1
            fi
        fi
    done

    unset i
    unset pathmunge
fi
# vim:ts=4:sw=4',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(98,61,'/bash/env','p','另外该文件也会执行/etc/profile.d/*.sh来设定特定应用程序的环境变量。其实登录式shell也会执行$HOME/.bashrc，可以回到上面的~/.bash_profile的代码部分，我们会发现该文件中会调用$HOME/.bashrc文件。这样说可以加深登录式shell和非登录式shell的本质区别。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(99,62,'/bash/env','h4','3、交互式shell',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(100,63,'/bash/env','p','我们通过终端登录Linux，输入命令，shell执行命令并实时返回结果，退出。这种模式就是交互式shell。在交互式shell下，bash不会执行/etc/profile文件，代替而之的是$HOME/.bashrc文件,执行的启动文件和非登录式shell一样。这个文件定义新交互式shell的环境变量，该文件最好不要定义全局环境变量（export），另外该文件也会执行/etc/profile.d/*.sh来设定特定应用程序的环境变量。任何开启交互式子shell(bash、su- user)的操作都会读取$HOME/.bashrc。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(101,64,'/bash/env','h4','4、非交互式shell',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(102,65,'/bash/env','p','和交互式shell相反，该模式下shell不与终端进行交互，例如以shell脚本的方式读取脚本中命令，而不需要与终端交互（除非需要用户输入参数的命令），当文件结束时，该shell也就退出了。非交互式shell的相关启动文件和系统设置的一个全局环境变量BASH_ENV相关。该变量默认情况下没有定义。我们需要手动设置该变量，当执行shell脚本的时候，会执行该变量指向的文件。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(103,66,'/bash/env','p','我们可以利用$-的变量值来查看当前shell是交互式还是非交互式的，如下图：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(104,67,'/bash/env','pre','vim tmp.sh
#!/bin/bash
echo $-',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(105,68,'/bash/env','pre','[root@CentOS6 bin]# bash tmp.sh
hB                           # 非交互式shell
[root@CentOS6 bin]# echo $-
himBH                        # 交互式shell
[root@CentOS6 bin]#',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(106,69,'/bash/env','h4','5、 总结',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(107,70,'/bash/env','p','登录式shell,包括依次要执行的启动文件和文件代码部分要调用的文件，对他们概括如下：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(108,71,'/bash/env','img','/static/img/bash/env_01.png',null,null,null,null,null,null,'width=>900|height=>100|alt=>登录式shell执行启动文件',0,'alvin','1900-01-01');
insert into BookArticle values(109,72,'/bash/env','p','非登录式shell',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(110,73,'/bash/env','img','/static/img/bash/env_02.png',null,null,null,null,null,null,'width=>900|height=>100|alt=>非登录式shell执行启动文件',0,'alvin','1900-01-01');
insert into BookArticle values(111,74,'/bash/env','h5','交互式shell',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(112,75,'/bash/env','p','执行启动文件过程类似于非登录式shell',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(113,76,'/bash/env','h5','非交互式shell',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(114,77,'/bash/env','p','执行BASH_ENV全局环境变量指向的文件',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(115,78,'/bash/env','p','知道了这些启动文件的区别后，我们可以针对性的修改启动文件以使自定义的全局环境变量、别名等永久生效，例如我们可以将所有自定义的全局环境变量放在一个.sh结尾的文件中，然后将该文件放到/etc/profile.d/目录下或者将自定义的变量放入/etc/bashrc文件中，这样将对所有的用户都生效。而对于一些针对个人用户的别名等，可以将其写入到~/.bashrc文件中，只对单个用户有效。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');

insert into BookArticle values(116,1,'/bash/string','p','字符串是shell编程中最常用最有用的数据类型（除了数字和字符串，也没啥其它类型好用了），字符串可以用单引号，也可以用双引号，也可以不用引号。单双引号的区别跟PHP类似。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(117,2,'/bash/string','h3','单引号',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(118,3,'/bash/string','pre','str=\'this is a string\'',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(119,4,'/bash/string','p','单引号字符串的限制：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(120,5,'/bash/string','ul','单引号里的任何字符都会原样输出，单引号字符串中的变量是无效的；
单引号字串中不能出现单独一个的单引号（对单引号使用转义符后也不行），但可成对出现，作为字符串拼接使用。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(121,6,'/bash/string','h3','双引号',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(122,7,'/bash/string','pre','your_name=\'runoob\'
str="Hello, I know you are \"$your_name\"! \n"
echo -e $str',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(123,8,'/bash/string','p','输出结果为：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(124,9,'/bash/string','pre','Hello, I know you are "runoob"! ',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(125,10,'/bash/string','p','双引号的优点：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(126,11,'/bash/string','ul','双引号里可以有变量
双引号里可以出现转义字符',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(127,12,'/bash/string','h3','拼接字符串',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(128,13,'/bash/string','pre','your_name="runoob"
# 使用双引号拼接
greeting="hello, "$your_name" !"
greeting_1="hello, ${your_name} !"
echo $greeting  $greeting_1
# 使用单引号拼接
greeting_2=\'hello, \'$your_name\' !\'
greeting_3=\'hello, ${your_name} !\'
echo $greeting_2  $greeting_3',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(129,14,'/bash/string','p','输出结果为：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(130,15,'/bash/string','pre','hello, runoob ! hello, runoob !
hello, runoob ! hello, ${your_name} !',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(131,16,'/bash/string','h3','获取字符串长度',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(132,17,'/bash/string','pre','string="abcd"
echo ${#string} #输出 4',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(133,18,'/bash/string','h3','提取子字符串',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(134,19,'/bash/string','p','以下实例从字符串第 2个字符开始截取4个字符：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(135,20,'/bash/string','pre','string="runoob is a great site"
echo ${string:1:4} # 输出 unoo',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(136,21,'/bash/string','h3','查找子字符串',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(137,22,'/bash/string','p','查找字符 i或 o的位置(哪个字母先出现就计算哪个)：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(138,23,'/bash/string','pre','string="runoob is a great site"
echo `expr index "$string" io`  # 输出 4',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(139,24,'/bash/string','p','注意： 以上脚本中 `是反引号,而不是单引号 \',不要看错了哦.',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(140,25,'/bash/string','p','使用expr命令时，表达式中的运算符左右必须包含空格，如果不包含空格，将会输出表达式本身:',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(141,26,'/bash/string','pre','expr 5+6    // 直接输出 5+6
expr 5 + 6       // 输出 11',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(142,27,'/bash/string','p','对于某些运算符，还需要我们使用符号"\"进行转义，否则就会提示语法错误。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(143,28,'/bash/string','pre','expr 5 * 6       // 输出错误
expr 5 \* 6      // 输出30',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(144,29,'/bash/string','hr','',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(145,30,'/bash/string','strong','假设有变量 var=http://www.aaa.com/123.htm，实例如下：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(146,31,'/bash/string','strong','1. # 号截取，从左开始匹配的第一个字符，删除包含匹配字符的所有左边字符，保留右边字符。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(147,32,'/bash/string','pre','echo ${var#*//}',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(148,33,'/bash/string','p','其中 var 是变量名，# 号是运算符，*// 表示从左边开始删除第一个 // 号及左边的所有字符',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(149,34,'/bash/string','p','即删除 http://',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(150,35,'/bash/string','p','结果是 ：www.aaa.com/123.htm',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(151,36,'/bash/string','strong','2. ## 号截取，从左开始匹配的最后一个字符，删除包含匹配字符的左边字符，保留右边字符。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(152,37,'/bash/string','pre','echo ${var##*/}',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(153,38,'/bash/string','p','##*/ 表示从左边开始删除最后（最右边）一个 / 号及左边的所有字符',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(154,39,'/bash/string','p','即删除 http://www.aaa.com/',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(155,40,'/bash/string','p','结果是 123.htm',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(156,41,'/bash/string','strong','3. %号截取，从右开始匹配的第一个字符，删除包含匹配字符的右边字符，保留左边字符',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(157,42,'/bash/string','pre','echo ${var%/*}',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(158,43,'/bash/string','p','%/* 表示从右边开始，删除第一个 / 号及右边的字符',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(159,44,'/bash/string','p','结果是：http://www.aaa.com',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(160,45,'/bash/string','strong','4. %% 号截取，从右开始匹配的最后一个字符，删除包含匹配字符的右边字符，保留左边字符',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(161,46,'/bash/string','pre','echo ${var%%/*}',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(162,47,'/bash/string','p','%%/* 表示从右边开始，删除最后（最左边）一个 / 号及右边的字符',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(163,48,'/bash/string','p','结果是：http:',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(164,49,'/bash/string','strong','5. 从左边第几个字符开始，及字符的个数',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(165,50,'/bash/string','pre','echo ${var:0:5}',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(166,51,'/bash/string','p','其中的 0 表示左边第一个字符开始，5 表示字符的总个数。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(167,52,'/bash/string','p','结果是：http:',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(168,53,'/bash/string','strong','6. 从左边第几个字符开始，一直到结束。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(169,54,'/bash/string','pre','echo ${var:7}',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(170,55,'/bash/string','p','其中的 7 表示左边第8个字符开始，一直到结束。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(171,56,'/bash/string','p','结果是 ：www.aaa.com/123.htm',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(172,57,'/bash/string','strong','7. 从右边第几个字符开始，及字符的个数',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(173,58,'/bash/string','pre','echo ${var:0-7}',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(174,59,'/bash/string','p','其中的 0-7 表示右边算起第七个字符开始，3 表示字符的个数。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(175,60,'/bash/string','p','结果是：123',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(176,61,'/bash/string','strong','8. 从右边第几个字符开始，一直到结束。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(177,62,'/bash/string','pre','string="hello,everyone my name is xiaoming"
expr length "$string"',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(178,63,'/bash/string','p','表示从右边第七个字符开始，一直到结束。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(179,64,'/bash/string','p','结果是：123.htm',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(180,65,'/bash/string','em','注：（左边的第一个字符是用 0 表示，右边的第一个字符用 0-1 表示）',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(181,66,'/bash/string','strong','9. 计算字符长度也可是使用 length:',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(182,67,'/bash/string','pre','string="hello,everyone my name is xiaoming"
expr length "$string"',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(183,68,'/bash/string','p','输出:34',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(184,69,'/bash/string','p','注意：string字符串里边有空格,所以需要添加双引号',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(185,70,'/bash/string','strong','10. 字符串大小写',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(186,71,'/bash/string','pre','var="Hello,Word"',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(187,72,'/bash/string','pre','echo ${var^}     # 把变量中的第一个字符换成大写 
echo ${var^^}    # 把变量中的所有小写字母，全部替换为大写
echo ${var,}     # 把变量中的第一个字符换成小写
echo ${var,,}    # 把变量中的所有大写字母，全部替换为小写',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(188,73,'/bash/string','p','输出:',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(189,74,'/bash/string','pre','Hello,Word
HELLO,WORD
hello,Word
hello,word',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(190,1,'/bash/comment','p','以 #开头的行就是注释，会被解释器忽略。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(191,2,'/bash/comment','p','通过每一行加一个#号设置多行注释，像这样：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(192,3,'/bash/comment','pre','#--------------------------------------------
# 这是一个注释
# author：菜鸟教程
# site：www.runoob.com
# slogan：学的不仅是技术，更是梦想！
#--------------------------------------------
##### 用户配置区 开始 #####
#
#
# 这里可以添加脚本描述信息
# 
#
##### 用户配置区 结束  #####',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(193,4,'/bash/comment','p','如果在开发过程中，遇到大段的代码需要临时注释起来，过一会儿又取消注释，怎么办呢？',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(194,5,'/bash/comment','p','每一行加个#符号太费力了，可以把这一段要注释的代码用一对花括号括起来，定义成一个函数，没有地方调用这个函数，这块代码就不会执行，达到了和注释一样的效果。',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(195,6,'/bash/comment','h3','多行注释',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(196,7,'/bash/comment','p','多行注释还可以使用以下格式：',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(197,8,'/bash/comment','pre',':<<EOF
注释内容...
注释内容...
注释内容...
EOF',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(198,9,'/bash/comment','p','EOF 也可以使用其他符号:',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
insert into BookArticle values(199,10,'/bash/comment','pre',':<<\'
注释内容...
注释内容...
注释内容...
\'

:<<!
注释内容...
注释内容...
注释内容...
!',null,null,null,null,null,null,null,0,'alvin','1900-01-01');
