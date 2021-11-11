# -*- coding: utf-8 -*-
'''
Created on 2021/11/11

@author: xcKev
'''
import mistune
import re
from tools import common_tools
class MarkDownReader(object):
    def __init__(self,markdown_text):
        self.markdown_text=markdown_text
        self.markdown_parser=mistune.BlockLexer(mistune.BlockGrammar())
        self.markdown_outputs=self.markdown_parser.parse(self.markdown_text)
        self.markdown_tokens=[]
    
    def get_markdown_correct_text(self,markdown_text):
        match_links=re.findall(r'\[(.*?)\]\((http.+)\)',markdown_text,flags=0)
        match_images=re.findall(r'!\[\]\((.+)\)',markdown_text,flags=0)
        if match_images:
            markdown_texts=[]
            for match_image in match_images:
                md_image="![]("+match_image+")"
                front_text=markdown_text.split(md_image)[0]
                if front_text != '':
                    markdown_texts.append({'markdown_key':'paragraph','markdown_val':front_text})
                markdown_texts.append({'markdown_key':'image','markdown_val':match_image})
                markdown_text=markdown_text.replace(front_text+md_image,'')
            return markdown_texts
        if match_links:
            markdown_texts=[]
            for match_link in match_links:
                match_link_key = match_link[0]
                match_link_val = match_link[1]
                match_link_k= "["+match_link_key+"]"+"("+match_link_val+")"
                front_text=markdown_text.split(match_link_k)[0]
                if front_text != '':
                    markdown_texts.append({'markdown_key':'paragraph','markdown_val':front_text})
                markdown_texts.append({'markdown_key':'link','markdown_val':{match_link_key:match_link_val}})
                markdown_text=markdown_text.replace(front_text,'')
            return markdown_texts
        return markdown_text
    
    def process_markdown_token(self,markdown_output):
        markdown_type = markdown_output['type']
        markdown_text = ''
        if 'text' in markdown_output.keys():
            markdown_text = self.get_markdown_correct_text(markdown_output['text'])
        token=dict()
        if markdown_type == 'heading':
            markdown_key=markdown_type+str(markdown_output['level'])
            token['markdown_key']=markdown_key
            token['markdown_val']=markdown_text
            self.markdown_tokens.append(token)
        elif markdown_type == 'hrule':
            token['markdown_key']='hr'
            token['markdown_val']=''
            self.markdown_tokens.append(token)
        elif markdown_type == 'paragraph':
            if common_tools.is_list(markdown_text):
                for single_token in markdown_text:
                    self.markdown_tokens.append(single_token)
            else:
                token['markdown_key']='paragraph'
                token['markdown_val']=markdown_text
                self.markdown_tokens.append(token)
        elif markdown_type == 'table':
            markdown_val=[markdown_output['header']]
            for cell in markdown_output['cells']:
                markdown_val.append(cell)
            token['markdown_key']='table'
            token['markdown_val']=markdown_val
            self.markdown_tokens.append(token)
        elif markdown_type =='code':
            token['markdown_type']='code'
            token['markdown_val']=markdown_text
            self.markdown_tokens.append(token)
        
    def read_markdown(self):
        oul_token=dict()
        for markdown_output in self.markdown_outputs:
            markdown_type = markdown_output['type']
            if markdown_type in ('heading','hrule','paragraph','table','code'):
                self.process_markdown_token(markdown_output)
                
            elif markdown_type=='list_start':
                oul_token['markdown_key']='ul'
                if markdown_output['ordered']:
                    oul_token['markdown_key']='ol'
                oul_token['markdown_val']=[]
            elif markdown_type in ('list_item_start','list_item_end'):
                continue
            elif markdown_type == 'text' and 'markdown_key' in oul_token.keys():
                oul_token['markdown_val'].append(self.get_markdown_correct_text(markdown_output['text']))
            elif markdown_type == 'list_end':
                self.markdown_tokens.append(oul_token)
                oul_token=dict()
        return self.markdown_tokens
        
if __name__=='__main__':
    markdown_reader=MarkDownReader('''
# Linux 部署安装


本章节我们将为大家介绍 Linux 的安装。
本章节以 Centos6.4 与Centos7 为例。
接下来你需要将下载的Linux系统刻录成光盘或U盘或使用VMware虚拟机安装ISO文件。
Centos 下载地址：
 可以去官网下载[最新版本：https://www.centos.org/download/](https://www.centos.org/download/)

![](/media/img/linux/linux_install.jpg)

* **  注： ** 建议安装64位Linux系统。*
* [旧版本下载地址：https://wiki.centos.org/Download](https://wiki.centos.org/Download)

---

## 常用查看系统命令
### 1、查看系统版本
    cat /etc/centos.release
    cat /etc/redhat.release

---
## Window上安装VMware虚拟机
1、首先，运行下载完成的 Vmware Workstation 虚拟机软件包，    将会看到如图所示的虚拟机程序安装向导初始界面。
![](/media/img/linux/linux_vm_install_img_001.png)
2、在虚拟机软件的安装向导界面单击"下一步"按钮
![](/media/img/linux/linux_vm_install_img_002.png)
3、在最终用户许可协议界面选中"我接受的条款"复框，然后单击下一步按钮
![](/media/img/linux/linux_vm_install_img_003.png)
4、选择虚拟机软件的安装位置（可默认），中"增强型键盘驱动程序"复框后单击"下一步"按钮
![](/media/img/linux/linux_vm_install_img_004.png)
5、根据自身情况适当选择"启动时检查产品更新"与帮助完善 根据自身情况适当选择“启动时检查产品更新”与帮助完善VMware Workstation Pro”复选框，然后单击“下一步”按钮
![](/media/img/linux/linux_vm_install_img_005.png)
6、选中"桌面"和"开始菜单程序文件夹"复框，然后击下一步按钮
![](/media/img/linux/linux_vm_install_img_006.png)
7、一切准备就绪后，单击"安装"按钮
![](/media/img/linux/linux_vm_install_img_007.png)
8、进入安装过程，此时要做的就是耐心等待虚拟机软件结束
![](/media/img/linux/linux_vm_install_img_008.png)
9、大约 5～10分钟后，虚拟机软件便会安装完成，然后再次单击"完成"按钮
![](/media/img/linux/linux_vm_install_img_009.png)
10、双击桌面上生成的虚拟机快捷图标，在弹出的界面，输入许可证密钥，或者选择试用之后，单击"继续"按钮（这里选择的是"我希望VMware Workstation 12 30天"复选框）。
![](/media/img/linux/linux_vm_install_img_010.png)
11、在出现"欢迎使用 VMware Workstation 12"界面后，单击"完成按钮"。
![](/media/img/linux/linux_vm_install_img_011.png)
12、在桌面上再次双击快捷方式，此时便看到了虚拟机软件的管理界面。
***注意，在安装完虚拟机之后，不能立即安装Linux系统，因为还要在虚拟机内设置操作系统的硬件标准。只有把虚拟机内资源模出来后才可以正式步入Linux系统安装之旅。VM虚拟机的强大之处在于不仅可以调取真实的物理设备资源，还可以模拟出多网卡或硬盘等资源，因此完全可以满足大家对学习环境的需求，再次强调，真的不用特意购买电脑。***
![](/media/img/linux/linux_vm_install_img_012.png)
13、单击"创建新的虚拟机"选项，并在弹出的"新建虚拟机向导"界面中选择"典型"单选按钮，然后单击"下一步"按钮。
![](/media/img/linux/linux_vm_install_img_013.png)
14、选中"稍后安装操作系统"单选按钮，然单击"下一步"。
![](/media/img/linux/linux_vm_install_img_014.png)
15、将客户机操作系统的类型选择为"Linux",版本为"Red Hat Enterprise Linux 7 64位"，然后单击“下一步”按钮。
![](/media/img/linux/linux_vm_install_img_015.png)
16、填写“虚拟机名称”字段，并在选择安装位置之后单击“下一步”按钮。
![](/media/img/linux/linux_vm_install_img_016.png)
17、将虚拟机系统的“最大磁盘大小”设置为 20.0GB（默认即可），然后单击“下一步”按钮。
![](/media/img/linux/linux_vm_install_img_017.png)
18、单击“自定义硬件”按钮。
![](/media/img/linux/linux_vm_install_img_018.png)
19、在出现的图所示的界面中，建议将虚拟机系统内存的可用量设置为 2GB，最低不应低于 1GB。如果自己的真机设备具有很强的性能，那么也建议将内存量设置为 2GB，因为将虚拟机系统的内存设置得太大没有必要。
![](/media/img/linux/linux_vm_install_img_019.png)
20、根据您真机的性能设置 CPU 处理器的数量以及每个处理器的核心数量，并开启虚拟化功能。
![](/media/img/linux/linux_vm_install_img_020.png)
21、光驱设备此时应在“使用 ISO 镜像文件”中选中了下载好的 RHEL 系统镜像文件。
![](/media/img/linux/linux_vm_install_img_021.png)
22、VM 虚拟机软件为用户提供了 3 种可选的网络模式，分别为桥接模式、NAT 模式与仅主机模式。这里选择“仅主机模式”。
 ➢桥接模式： 相当于在物理主机与虚拟机网卡之间架设了一座桥梁，从而可以通过物理主机的网卡访问外网。
 ➢NAT模式： 让 VM 虚拟机的网络服务发挥路由器的作用，使得通过虚拟机软件模拟的主机可以通过物理主机访问外网，在真机中 NAT 虚拟机网卡对应的物理网卡是VMnet8。 
 ➢仅主机模式： 仅让虚拟机内的主机与物理主机通信，不能访问外网，在真机中仅主机模式模拟网卡对应的物理网卡是 VMnet1。
![](/media/img/linux/linux_vm_install_img_022.png)
23、把 USB 控制器、声卡、打印机设备等不需要的设备统统移除掉。移掉声卡后可以避免在输入错误后发出提示声音，确保自己在今后实验中思绪不被打扰。然后单击“关闭”按钮。

![](/media/img/linux/linux_vm_install_img_023.png)
24、返回到虚拟机配置向导界面后单击“完成”按钮，如图所示。虚拟机的安装和配置顺利完成。
![](/media/img/linux/linux_vm_install_img_024.png)

25、当看到如图所示的界面时，就说明您的虚拟机已经被配置成功了。接下来准备步入属于您的 Linux 系统之旅吧。
![](/media/img/linux/linux_vm_install_img_025.png)

## Linux 6.4 安装步骤
1、首先，使用光驱或U盘或你下载的Linux ISO文件进行安装。
界面说明：
![](/media/img/linux/linux_install_img_001.png)

    Install or upgrade an existing system 安装或升级现有的系统
    install system with basic video driver 安装过程中采用基本的显卡驱动
    Rescue installed system 进入系统修复模式
    Boot from local drive   退出安装从硬盘启动
    Memory test  内存检测

注：用联想E49安装时选择第一项安装时会出现屏幕显示异常的问题，后改用第二项安装时就没有出现问题
2、这时直接"skip"就可以了
![](/media/img/linux/linux_install_img_002.png)
3、出现引导界面，点击"next"
![](/media/img/linux/linux_install_img_003.png)
4、选中"English（English）"否则会有部分乱码问题
![](/media/img/linux/linux_install_img_004.png)
5、键盘布局选择"U.S.English"
![](/media/img/linux/linux_install_img_005.png)
6、选择"Basic Storage Devices"点击"Next"
![](/media/img/linux/linux_install_img_006.png)
7、询问是否忽略所有数据，新电脑安装系统选择"Yes,discard any data"
![](/media/img/linux/linux_install_img_007.png)
8、Hostname填写格式"英文名.姓"
![](/media/img/linux/linux_install_img_008.png)
9、网络设置安装图示顺序点击就可以了
![](/media/img/linux/linux_install_img_009.png)
10、时区可以在地图上点击，选择"shanghai"并取消System clock uses UTC前面的对勾
![](/media/img/linux/linux_install_img_010.png)
11、设置root的密码
![](/media/img/linux/linux_install_img_011.png)
12、硬盘分区，一定要按照图示点选
![](/media/img/linux/linux_install_img_012.png)
13、调整分区，必须要有/home这个分区，如果没有这个分区，安装部分软件会出现不能安装的问题
![](/media/img/linux/linux_install_img_013.png)
14、询问是否格式化分区
![](/media/img/linux/linux_install_img_014.png)
15、将更改写入到硬盘
![](/media/img/linux/linux_install_img_015.png)
16、引导程序安装位置
![](/media/img/linux/linux_install_img_016.png)
17、最重要的一步，也是本教程最关键的一步，也是其他教程没有提及的一步，按图示顺序点击
![](/media/img/linux/linux_install_img_017.png)
18、取消以下内容的所有选项
Applications
Base System
Servers
并对Desktops进行如下设置
即取消如下选项：
Desktop Debugging and Performance Tools
Desktop Platform
Remote Desktop Clients
 **  Input Methods ** **  中仅保留ibus-pinyin-1.3.8-1.el6.x86_64,其他的全部取消 **
![](/media/img/linux/linux_install_img_018.png)
![](/media/img/linux/linux_install_img_019.png)
19、选中Languages，并选中右侧的Chinese Support然后点击红色区域
![](/media/img/linux/linux_install_img_020.png)
20、调整完成后如下图所示
![](/media/img/linux/linux_install_img_021.png)
21、至此，一个最精简的桌面环境就设置完成了，
![](/media/img/linux/linux_install_img_022.png)
22、安装完成，重启
![](/media/img/linux/linux_install_img_023.png)
23、重启之后，的License Information
![](/media/img/linux/linux_install_img_024.png)
24、Create User
Username：填写您的英文名（不带.姓）
Full Name：填写您的英文名.姓（首字母大写）
![](/media/img/linux/linux_install_img_025.png)
25、"Date and Time" 选中 "Synchronize data and time over the network"
Finsh之后系统将重启
![](/media/img/linux/linux_install_img_026.png)
26、第一次登录，登录前不要做任何更改，这个很重要！！！登录之后紧接着退出
第二次登录，选择语言，在红色区域选择下拉小三角，选other，选中"汉语（中国）"
![](/media/img/linux/linux_install_img_027.png)
![](/media/img/linux/linux_install_img_028.png)
27、登录之后，请一定按照如下顺序点击！
至此，CentOS安装完成，如有其他问题，请随时与我联系！！
![](/media/img/linux/linux_install_img_029.png)

---

## Linux 7 安装步骤


1、选择好ISO文件，按回车键后开始加载安装镜像，所需时间大约在 30～60 秒，请耐心等待。
![](/media/img/linux/linux_install7_img_001.png)
![](/media/img/linux/linux_install7_img_002.png)
2、选择系统的安装语言后单击 Continue 按钮。
![](/media/img/linux/linux_install7_img_003.png)
3、在安装界面中单击 SOFTWARE SELECTION 选项。
![](/media/img/linux/linux_install7_img_004.png)
4、CentOS 7 系统的软件定制界面可以根据用户的需求来调整系统的基本环境，例如把 Linux 系统用作基础服务器、文件服务器、Web 服务器或工作站等。此时您只需在界面中单击选中 Server with GUI 单选按钮，然后单击左上角的 Done 按钮即可。
![](/media/img/linux/linux_install7_img_005.png)
5、返回到 CentOS 7 系统安装主界面，单击 NETWORK & HOSTNAME 选项后，将 Hostname字段设置为 linuxprobe.com，然后单击左上角的 Done 按钮。
![](/media/img/linux/linux_install7_img_006.png)
6、返回到安装主界面，单击 INSTALLATION DESTINATION 选项来选择安装媒介并设置分区。此时不需要进行任何修改，单击左上角的 Done 按钮即可。
![](/media/img/linux/linux_install7_img_007.png)
7、返回到安装主界面，单击 Begin Installation 按钮后即可看到安装进度，在此处选择 ROOT PASSWORD。
![](/media/img/linux/linux_install7_img_008.png)
8、然后设置root管理员的密码。若坚持用弱口令的密码则需要单击2次左上角的Done按钮才可以确认，如图所示。
这里需要多说一句，当您在虚拟机中做实验的时候，密码无所谓强弱，但在生产环境中一定要让root管理员的密码足够复杂，否则系统将面临严重的安全问题。
![](/media/img/linux/linux_install7_img_009.png)
9、Linux系统安装过程一般在30～60分钟，在安装过程期间耐心等待即可。安装完成后单 击Reboot按钮
![](/media/img/linux/linux_install7_img_010.png)
10、重启系统后将看到系统的初始化界面，单击LICENSEINFORMATION选项。
![](/media/img/linux/linux_install7_img_011.png)
11、选中Iacceptthelicenseagreement复选框，然后单击左上角的Done按钮。
![](/media/img/linux/linux_install7_img_012.png)
12、返回到初始化界面后单击FINISHCONFIGURATION选项，即可看到Kdump服务的设置界面。如果暂时不打算调试系统内核，也可以取消选中Enablekdump复选框，然后单击Forward按钮。
![](/media/img/linux/linux_install7_img_013.png)
13、在如图所示的系统订阅界面中，选中No,I prefer to register at a later time单选按钮，然后单击Finish按钮。此处设置为不注册系统对后续的实验操作和生产工作均无影响。
![](/media/img/linux/linux_install7_img_014.png)
14、虚拟机软件中的RHEL7系统经过又一次的重启后，我们终于可以看到系统的欢迎 界面，如图所示。在界面中选择默认的语言English(UnitedStates)，然后单击Next 按钮。
![](/media/img/linux/linux_install7_img_015.png)
15、将系统的输入来源类型选择为English(US)，然后单击Next按钮
![](/media/img/linux/linux_install7_img_016.png)
16、为RHEL7系统创建一个本地的普通用户，该账户的用户名为linuxprobe，密码为redhat，然后单击Next按钮，如图所示。
![](/media/img/linux/linux_install7_img_017.png)
17、按照图所示的设置来设置系统的时区，然后单击Next按钮。
![](/media/img/linux/linux_install7_img_018.png)
18、在图所示的界面中单击Start using RedHat Enterprise Linux Server按钮，出现如图所示的界面。至此，RHEL7系统完成了全部的安装和部署工作。准备开始学习Linux系统吧。
![](/media/img/linux/linux_install7_img_019.png)
![](/media/img/linux/linux_install7_img_020.png)
'''
    )
    markdown_outputs=markdown_reader.read_markdown()
    for output in markdown_outputs:
        print(output)