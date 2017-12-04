#-*-coding;gbk-*-
import base64
import os
def getConf():
    confs = ['user_list_path','video_path','sort_index','user','pwd'] #用户列表路径，视频路径，视频分类索引
    path = os.getcwd()
    filename = path +r'\conf.txt'
    f = open(filename,'a+')
    f.seek(0,0)
    lines = f.readlines()
    f.close()
    conf = {}
    for line in lines:
        line = line.strip().replace('\n','')
        if ':' in line:
            l = line.split(':')
            key = l[0]
            value = l[1]
            try:
                value = base64.b64decode(l[1]).decode()
            except Exception as e:
                value = ''
            conf.update({key:value})
    for x in confs:
        if x not in conf:
            conf.update({x:''})
    return(conf)
def writeConf(conf):
    path = os.getcwd()
    filename = path + '\\conf.txt'
    f = open(filename,'w')
    for c in conf:
        value = base64.b64encode(conf[c].encode(encoding='utf-8')).decode()

        txt = c + ':' + value + '\n'
        f.write(txt)

    f.close()
# t = {'user_list_path': '11path1', 'video_path': '22path2', 'bbb': ''}
# writeConf(t)
# getConf()
