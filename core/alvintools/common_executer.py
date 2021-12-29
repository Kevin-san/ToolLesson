# -*- coding: UTF-8 -*-
'''
Created on 2021/4/3

@author: xcKev
'''
import docker
import re
from tools import common_tools



class Executor():
    def __init__(self):
        self.dock_client=docker.from_env()
        if common_tools.get_system_name() == "Linux":
            self.exec_client = docker.APIClient(base_url='unix:///var/run/docker.sock')
        else:
            self.exec_client=docker.APIClient(base_url='tcp://localhost:2375')
    
    def get_container(self,image_name):
        self.exec_client.start(image_name)
        return self.dock_client.containers.get(image_name)
    
    def stop_container(self,container):
        container.stop()
    
    def run_python(self,cmds):
        container=self.get_container('python')
        exec_results=[]
        real_cmds=['/bin/bash','touch /tmp/test.py',['sh','-c','echo "#!/usr/bin/python" > /tmp/test.py']]
        for cmd in cmds:
            cmd=cmd.replace('"','\\"')
            real_cmds.append(['sh','-c','echo '+'"'+cmd+'"'+' >> /tmp/test.py'])
        real_cmds.append("chmod +x /tmp/test.py")
        real_cmds.append("/tmp/test.py")
        for real_cmd in real_cmds:
            exec_results.append(container.exec_run(real_cmd))
        self.stop_container(container)
        return exec_results
    
    def run_perl(self,cmds):
        container=self.get_container("perl")
        exec_results=[]
        real_cmds=['/bin/bash','touch /tmp/test.pl',['sh','-c','echo "#!/usr/local/bin/perl" > /tmp/test.pl']]
        for cmd in cmds:
            cmd=cmd.replace('"','\\"')
            real_cmds.append(['sh','-c','echo '+'"'+cmd+'"'+' >> /tmp/test.pl'])
        real_cmds.append("chmod +x /tmp/test.pl")
        real_cmds.append("/tmp/test.pl")
        for real_cmd in real_cmds:
            exec_results.append(container.exec_run(real_cmd))
        self.stop_container(container)
        return exec_results
    
    def run_golang(self,cmds):
        container=self.get_container("golang")
        real_cmds=["rm -rf /tmp/test.go","touch /tmp/test.go"]
        exec_results=[]
        for cmd in cmds:
            cmd=cmd.replace('"','\\"')
            real_cmds.append(['sh','-c','echo '+'"'+cmd+'"'+' >> /tmp/test.go'])
        real_cmds.append('chmod +x /tmp/test.go')
        real_cmds.append('go run /tmp/test.go')
        for real_cmd in real_cmds:
            exec_results.append(container.exec_run(real_cmd))
        self.stop_container(container)
        return exec_results
    
    def run_bash(self,cmds):
        container=self.get_container("bash")
        real_cmds=["bash"]
        exec_results=[]
        for cmd in cmds:
            cmd=cmd.replace('"','\\"')
            real_cmds.append(['sh','-c',cmd])
        for real_cmd in real_cmds:
            exec_results.append(container.exec_run(real_cmd))
        self.stop_container(container)
        return exec_results
    
    def run_java(self,cmds):
        container=self.get_container("java")
        real_cmds=["rm -rf /tmp/Test.java","touch /tmp/Test.java"]
        exec_results=[]
        cmd='\n'.join(cmds)
        cmd=cmd.replace('"','\\"')
        rpl_str=re.search(r' class (\w+)\s*{',cmd).group(0)
        cmd=cmd.replace(rpl_str,' class Test {')
        real_cmds.append(['sh','-c','echo '+'"'+cmd+'"'+' >> /tmp/Test.java'])
        real_cmds.append('javac /tmp/Test.java')
        real_cmds.append('chmod +x /tmp/Test.class')
        real_cmds.append('java Test')
        for real_cmd in real_cmds:
            exec_results.append(container.exec_run(real_cmd,environment={'CLASSPATH':'$JAVA_HOME/jre/lib/ext:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/alvintools.jar:/tmp'}))
        self.stop_container(container)
        return exec_results
    
    def run_node(self,cmds):
        container=self.get_container("node")
        real_cmds=["rm -rf /tmp/test.js","touch /tmp/test.js"]
        exec_results=[]
        for cmd in cmds:
            cmd=cmd.replace('"','\\"')
            real_cmds.append(['sh','-c','echo '+'"'+cmd+'"'+' >> /tmp/test.js'])
        real_cmds.append('chmod +x /tmp/test.js')
        real_cmds.append('node /tmp/test.js')
        for real_cmd in real_cmds:
            exec_results.append(container.exec_run(real_cmd))
        self.stop_container(container)
        return exec_results
        
common_exec=Executor()

def run_java(java_cmds):
    java_results=common_exec.run_java(java_cmds)
    java_result_strs=[]
    for exec_result in java_results:
        if exec_result.output != b'':
            java_result_strs.append(exec_result.output.decode())
    return "\n".join(java_result_strs)

def run_node_js(node_js_cmds):
    node_js_results=common_exec.run_node(node_js_cmds)
    node_js_result_strs=[]
    for exec_result in node_js_results:
        if exec_result.output != b'':
            node_js_result_strs.append(exec_result.output.decode())
    return "\n".join(node_js_result_strs)

def run_python(python_cmds):
    python_results=common_exec.run_python(python_cmds)
    python_result_strs=[]
    for exec_result in python_results:
        if exec_result.output != b'':
            python_result_strs.append(exec_result.output.decode())
    return "\n".join(python_result_strs)

def run_bash(bash_cmds):
    bash_results=common_exec.run_bash(bash_cmds)
    bash_result_strs=[]
    for exec_result in bash_results:
        if exec_result.output != b'':
            bash_result_strs.append(exec_result.output.decode())
    return "\n".join(bash_result_strs)

def run_perl(perl_cmds):
    perl_results=common_exec.run_perl(perl_cmds)
    perl_result_strs=[]
    for exec_result in perl_results:
        if exec_result.output != b'':
            perl_result_strs.append(exec_result.output.decode())
    return "\n".join(perl_result_strs)

def run_go(go_cmds):
    go_results=common_exec.run_golang(go_cmds)
    go_result_strs=[]
    for exec_result in go_results:
        if exec_result.output != b'':
            go_result_strs.append(exec_result.output.decode())
    return "\n".join(go_result_strs)
    