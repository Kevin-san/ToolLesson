import platform
def get_system_name():
    return platform.system()

def get_remote_folder():
    system_name = get_system_name()
    remote_map={"Windows":"I:","Linux":"/mnt/in"}
    return remote_map[system_name]

def get_ffmpeg_cmd():
    system_name = get_system_name()
    ffmpeg_map={"Windows":"E:/IDE/ffmpeg-2021-01-05/bin/ffmpeg.exe","Linux":"/usr/bin/ffmpeg"}
    return ffmpeg_map[system_name]

def get_holly_file():
    system_name = get_system_name()
    holly_map={"Windows":"C:/Users/xcKev/eclipse-workspace/KToolApps/test/holiy_cn.txt","Linux":"/usr/local/core_pdf_page/config/holiy_cn.txt"}
    return holly_map[system_name]