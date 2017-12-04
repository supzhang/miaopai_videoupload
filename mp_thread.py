# -*- coding: UTF-8 -*-
from PyQt5.QtCore import QThread,pyqtSignal
# from PyQt5.QtWidgets import QLabel,QTableWidgetItem,QGraphicsPixmapItem,QGraphicsScene,QGraphicsView
# from PyQt5.QtGui import QPixmap
from urllib import parse
import os,re,time,requests
import base64

class mp_thread(QThread):
    txtSignal = pyqtSignal(str)
    finishSignal = pyqtSignal(list)
    finishOkSignal = pyqtSignal()
    statusSignal = pyqtSignal(list)

    def __init__(self,sess,path,info,threadno,parent=None):
        super(mp_thread, self).__init__(parent)
        self.sess = sess
        self.path = path#.replace('_','-')
        self.info = info
        self.retry_times = 6
        self.threadno = threadno
        self.tooltip = '运行日志：'

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Cache-Control': 'max-age=0',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'Upgrade-Insecure-Requests': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://creator.miaopai.com/login',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        self.file_name = os.path.basename(path)
        self.finsig = [info['phone'], info['ftitle'], self.file_name]



    def run(self):
        init_upload_n = 0
        while True:#init_upload_n < self.retry_times:
            init_upload = self.init_upload()
           # print('init_upload', init_upload)
            time.sleep(0.3)
            self.statusChange(3,init_upload['msg'])
            if init_upload['init_ok'] == 0: #初始化失败，重新上初始化
                init_upload += 1
                if init_upload_n < self.retry_times:
                    txt = '初始化失败，重新初始化！重试次数：' + str(init_upload_n)
                    self.statusChange(2,txt)
                    continue
                else:
                    ftxt = '初始化失败，重新初始化！重试超过限制次数，停止上传'
                    self.finsig.append(ftxt)
                    self.statusChange(3,ftxt)
                    self.finishSignal.emit([0,self.finsig])
                    return

            #else: #初始化成功，开始上传
            checktitle = self.checkTitle()
            if checktitle['check_title_ok'] == 0:
                self.statusChange(2,checktitle['msg'])
                break

            self.statusChange(3,'开始上传文件!')
            upload_video_n = 0
            while True:#upload_video_n < self.retry_times:
                upload_videos = self.upload_video(self.path)
                self.statusChange(3,upload_videos['msg'])
                mkfile = self.mkfile()
                self.statusChange(3,mkfile['msg'])

                if upload_videos['upload_ok'] == 0 or mkfile['check_ok'] == 0: #如果上传失败
                    upload_video_n += 1
                    if upload_video_n < self.retry_times:
                        self.statusChange(3,'上传失败，重新上传数据，次数：' + str(upload_video_n))
                        continue
                    else:
                        ftxt = '上传失败，重试超过限制次数，停止上传'
                        self.statusChange(3,ftxt)
                        self.finsig.append(ftxt)
                        self.finishSignal.emit([0,self.finsig])
                        return

                else:
                    checkVideoStatus = self.checkVideoStatus()
                    time.sleep(0.3)
                    coverTrans = self.coverTrans(checkVideoStatus['w'],checkVideoStatus['h'])
                    time.sleep(0.3)
                    videoTransNew = self.videoTransNew(checkVideoStatus['w'],checkVideoStatus['h'])

                    self.statusChange(3,'正在等待获取封面地址,60秒内无法获取将停止...')

                    getCovers = self.getCovers()
                    print(getCovers)
                    if getCovers['getcover_ok'] == 1:
                        getUploadCoverimage = self.getCoverimage(getCovers['image_path'])
                        self.statusChange(3,getUploadCoverimage['msg'])
                        publishNew = self.publishNew(checkVideoStatus['w'],checkVideoStatus['h'])
                        self.statusChange(1,publishNew['msg'])
                        time.sleep(1)
                        self.finishOkSignal.emit()
                        return
                    elif getCovers['getcover_ok'] == 2:
                        try:
                            self.statusChange(2,'发现与视频文件同名图片，使用此图片做为封面！')
                        except Exception as e:
                            print(e)
                        upload_res = self.UploadCoverimage(getCovers['image'])
                        if upload_res['message'] == 'success':
                            time.sleep(1)
                            publishNew = self.publishNew(checkVideoStatus['w'],checkVideoStatus['h'])
                            self.statusChange(1,publishNew['msg'])
                            time.sleep(1)
                            self.finishOkSignal.emit()
                            return
                        else:
                            pass


                    else:
                        if upload_video_n < self.retry_times:
                            continue
                        else:
                            self.statusChange(2,'获取封面或发布失败！')
                            self.finsig.append('获取封面或发布失败！')
                            self.finishSignal.emit([0,self.finsig])
                            return
            if upload_video_n < self.retry_times:
                continue
            else:
                break
    def statusChange(self,status,msg):
        sig = {1:'成功',
               2:'失败',
               3:'运行中',
               4:'等待',
               5:'未开始'}
        self.tooltip = self.tooltip + '\n' + msg
        self.statusSignal.emit([self.threadno,sig[status],msg,self.tooltip])  #线程序号，状态，实时状态，提示



    # 初始化上传,获取新上传的token scid key等信息
    def init_upload(self):  #status=-1&device_name=web&width=480&height=480&slim=1&vend=qiniu_web_sdk
        self.headers['content-type'] = 'text/plain;charset=UTF-8'
        init_url = 'http://creator.miaopai.com/video/createNew'
        #data = 'status=-1&device_name=web&width=480&height=480&slim=1&vend=qiniu_web_sdk'
        data = {
            'status':'-1',
            'device_name':'web',
            'width':'480',
            'height':'480',
            'slim':'1',
            'vend':'qiniu_web_sdk'
        }
        try:
            res2 = self.sess.post(init_url,headers = self.headers,data = data,verify = False)
            res_json = res2.json()
        except Exception as e:
            msg = '上传初始化失败：' + str(e)
            return {
                'init_ok':0,
                'msg':msg,
                    }

        token = res_json['data']['media_token']
        self.scid = res_json['data']['scid']
        self.key = res_json['data']['image_base64key']
        self.image_key = res_json['data']['image_key']
        self.media_key = res_json['data']['media_key']
        ret = {
            'init_ok':1,
            'msg':'文件上传初始化成功！',
            'token':token,
            'scid':self.scid,
            'key':self.key,
            'image_key':self.image_key,
            'media_key':self.media_key,}
        return ret
    def checkTitle(self): #检查标题是否重复
        url_api = 'http://creator.miaopai.com/videocheck/checkTitle'
        url = url_api + '?title=' + self.info['ftitle'] +  '&scid=' + self.scid
        title_len = len(self.info['ftitle'])
        res = self.sess.get(url,headers = self.headers)
        res_json =res.json()
        if res_json['code'] == 200:
            check_title_ok = 1
            msg = '标题不重复，可正常使用！'
        else:
            check_title_ok = 0
            msg = '标题 重复，请重新输入！'#：' + self.info['ftitle'] +'

        ret = {
            'check_title_ok':check_title_ok,
            'msg':msg,

        }
        if len(self.info['title']) < 5:
            self.info['title'] = self.info['ftitle']
            self.statusChange(3,'描述为空，自动使用标题做为描述内容！')
        return ret
    #调用初始化，并上传数据，#all_info['path':文件路径,'sess':http线程,'user':用户名]
    def upload_video(self, path):
        self.headers['content-type'] = 'application/octet-stream'
        init_data = self.init_upload()
        self.headers.update({'Authorization': 'UpToken ' + init_data['token']})  # headers 中增加认证的部分
        self.file_size = os.path.getsize(path)  # 获取视频文件大小
        part_size = 4194304  # 分块上传的大小
        if part_size >= self.file_size:
            part_size = self.file_size
        sdk = 'qiniu_web_sdk'  # 验证时用到的SDK名称
        chunks = self.file_size // part_size
        chunks = str(chunks + 1) if self.file_size % part_size != 0 else chunks
        chunks = str(chunks)  # 一共分的块数
        if int(chunks) > 1:
            self.statusChange(3,'本视频共分 ' + chunks + '块上传！')
        part_no = 0  # 记录是第几个块
        file_name_re = re.search(r'.*/(.*)', path)
        self.file_name = file_name_re.group(1)
        f = open(path, 'rb')
        ctx_list = []  # 记录每次上传返回的ctx值
        while True:  # 上传每段视频
            if int(chunks) == part_no + 1:
                part_size = self.file_size - part_size * part_no
            upload_url = 'http://upload.qbox.me/mkblk/' + str(part_size) + '?name=' + parse.quote(self.file_name) + '&chunks=' + chunks + '&chunk=' + str(part_no)
            f_part = f.read(part_size)  # 只读取一块的大小
            part_no += 1

            try:
                if int(chunks) >= part_no:
                    if part_no == 1:
                        self.statusChange(3,'开始数据上传！')
                    upload_res = self.sess.post(upload_url, headers=self.headers, data=f_part, verify=False)
                    res_json = upload_res.json()
                    ctx_list.append(res_json['ctx'])
                    if int(chunks) > 0:
                        self.statusChange(3,'第 ' + str(part_no) + ' / ' + chunks +  ' 块上传完成！')
                else:
                    break

            except Exception as e:
                upload_ok = 0
                msg = '视频上传失败！'

        f.close()  # 关闭视频文件
        upload_ok = 1
        msg = '视频上传完毕！'
        self.ctx = ','.join(ctx_list)  # 获取上传结束后验证时的ctx字符串
        ret = {
            'upload_ok': upload_ok,
            'msg': msg}
        return ret
    def mkfile(self):  #检查文件是否上传正确self.headers['content-type'] = 'application/octet-stream'
        self.headers['content-type'] = 'text/plain;charset=UTF-8'
        #key_not_bin = 'stream/' + self.scid + '.mp4'
        key = base64.urlsafe_b64encode(self.media_key.encode(encoding='utf-8')).decode()
        fname = base64.urlsafe_b64encode(self.file_name.encode(encoding='utf-8')).decode()
        scid = base64.urlsafe_b64encode(self.scid.encode(encoding='utf-8')).decode()
        os_sdk = base64.urlsafe_b64encode('qiniu_web_sdk'.encode(encoding = 'utf-8')).decode()
        upload_time = base64.urlsafe_b64encode(str(int(time.time()*1000)).encode(encoding='utf-8')).decode()
        print(upload_time, type(upload_time))
         #上面将参数初始化，下面生成验证需要的URL
        url = 'http://upload.qbox.me/mkfile/' + str(self.file_size) + \
              '/key/' + key + \
              '/fname/' + fname + \
              '/x:scid/' + scid + \
              '/x:os/' + os_sdk + \
              '/x:upload_time/' + upload_time
        # print('key:',key)
        # print('self.key',self.key)
        # print('self.mediakey',self.media_key)
        # print('self.image_key',self.image_key)
        #print(self.ctx)
        retry_time2 = 2
        t = 0
        while t < retry_time2:
            try:
                check_res = self.sess.post(url,data = self.ctx,headers = self.headers,verify = False)
                check_json = check_res.json()

                hash = check_json['data']['hash']
                key = check_json['data']['key']
                msg = check_json['message']
                print(check_json)

                if msg == 'success':
                    check_ok = 1
                    msg = self.file_name + '文件检验完成！'
                else:
                    check_ok = 0
                    msg = self.file_name + '文件检验失败！'
                ret = {
                    'check_ok':check_ok,
                    'msg':msg,
                    'hash':hash,
                    'key':key,
                    }
                break

            except Exception as e:
                print(check_json)
                t += 1
                time.sleep(1)
                ret = {
                    'check_ok':0,
                    'msg':'文件校验失败！' + str(e)
                }
        return ret

    def checkVideoStatus(self):
        self.headers['content-type'] = 'application/x-www-form-urlencoded'
        url_api = 'http://creator.miaopai.com/video/checkVideoStatus'
        retry_times1 = 6
        t = 0
        while retry_times1 > t:
            try:
                res = self.sess.post(url_api, headers=self.headers, data={'scid': self.scid})
                check_status_ok = 1
                msg = '可以正常获取到上传视频的信息'
                res_json = res.json()
                print(res_json)

                h = res_json['data']['ext']['h']
                w = res_json['data']['ext']['w']
                break

            except Exception as e:
                check_status_ok = 0
                msg = '未能获取到数据上传的信息'
                h = ''
                w = ''
                t += 1
                time.sleep(1)
                print('exp',res_json)
        ret = {
            'check_status_ok': check_status_ok,
            'msg': msg,
            'w': w,
            'h': h,
        }
        return ret
    def coverTrans(self,w,h): #不知道干什么用，可能必须有才行，获取HASH后执行
        url_api = 'http://creator.miaopai.com/video/coverTrans'
        data = {
            'w': w,
            'h': h,
            'scid': self.scid,
        }
        covertrans = self.sess.post(url_api,data = data,headers = self.headers)
        return covertrans.json()
    def videoTransNew(self,w,h): #开始转码
        url_api = 'http://creator.miaopai.com/video/videoTransNew'

        data = {
            'w': w,
            'h': h,
            'scid': self.scid,
        }
        transnew_res = self.sess.post(url_api,data = data,headers = self.headers)
        transnew_json = transnew_res.json()
        msg = transnew_json['msg']
        data_res = transnew_json['data']
        transnew_ok = 1 if msg == '操作成功' else 0
        ret = {
            'transnew_ok':transnew_ok,
            'msg':'videoTransNew操作成功！',
            'data':data_res,
        }
        return ret
    def getCovers(self):
        self.headers['content-type'] = 'application/x-www-form-urlencoded'
        try:
            image = self.hasImage()

        except Exception as e:
            print(e)
        if image != 0:
            return {
                'getcover_ok':2,
                'image':image
            }
        t = 0 #计时，监测获取耗时
        url_api = 'http://creator.miaopai.com/video/getCovers'
        data = {
            'scid':self.scid,
        }
        while t < 80:
            t += 1
            try:
                cover_res = self.sess.post(url_api,headers = self.headers,data = data)
                cover_json = cover_res.json()
                image = cover_json['data']
                print(cover_json)
                image_path = ''
                image_name = ''
                if '没有这个' in cover_json['msg']:
                    getcover_ok = 0
                    msg = '视频上传失败！'
                    break
                else:
                    if len(image) > 1:
                        image_path = image[0]
                        r = re.search(r'.*(?<=/)(.*)', image_path)
                        image_name = r.group(1)
                        getcover_ok = 1
                        msg = '已经获取到封面图片地址！'
                        break
                    else:
                        getcover_ok = 0
                        msg = '未获取到封面图片！'
                        time.sleep(0.6)
            except Exception as e:
                 getcover_ok = 0
                 msg = '封面数据请求故障！'

        ret = {
            'getcover_ok':getcover_ok,
            'msg':msg,
            'image_path':image_path,
            'image_name':image_name,
        }
        return ret
    def hasImage(self):
        opath = self.path.replace(self.file_name,'')
        samepath = re.sub('\.[a-zA-Z0-9]{1,4}$','',self.path).replace('/','\\')
        for i in os.listdir(opath):
            FilePath = os.path.abspath(os.path.join(opath, i))
            if samepath in FilePath:
                if FilePath != self.path and FilePath.replace(samepath,'') in ['.png','.PNG','.JPG','.jpg','.bmp','.bmp','.jif','.GIF'] :
                    print(FilePath)
                    image = open(FilePath,'rb').read()
                    bimage = base64.b64encode(image)
                    return bimage
        return 0
        # res = self.sess.get(path, headers=self.headers)
        # image = res.content
        # bimage = base64.b64encode(image)
        # return bimage

    def getCoverimage(self,path):  #下载需要上传的图片

        try:
            res = self.sess.get(path,headers = self.headers)
            image = res.content
            bimage = base64.b64encode(image)
            uplooad_cover_ok = 1
            msg = '封面图片下载完成！'
            uploadok = self.UploadCoverimage(bimage)
            msg = '封面上传完成！'
        except Exception as e:
            uplooad_cover_ok  = 0
            msg = '封面图片下载或上传失败！'

        ret = {
            'uplooad_cover_ok':uplooad_cover_ok,
            'msg':msg,

        }

        return ret
    def UploadCoverimage(self,bimage):
        try:
            image_res = self.sess.post('http://up.qiniu.com/putb64/-1/key/' + self.key, headers=self.headers,
                                   data=bimage)  # 上传图片
            print(image_res.text)
            return image_res.json()
        except Exception as e:
            print(e)
            return {'message':'failed'}

    def publishNew(self,image_w,image_h):  #发布视频，填写标题等信息
        publish_url = 'http://creator.miaopai.com/video/publishNew'
        data = {
            'ftitle':self.info['ftitle'],
            'title': self.info['title'],
            'img': self.image_key,
            'scid': self.scid,
            'category': self.info['category'],
            'custom_tag': self.info['custom_tag'],
            'is_set_img': '0',
            'topics': self.info['topics'],
            'web_share': '0',
            'xkx_share': '0',
            'w': image_w,
            'h': image_h,
            'has_ad': self.info['hasad'],
            'is_original': self.info['orintal'],
            'is_serialize': self.info['serial'],
            'publish_time': '',
            'img_w': image_w,
            'img_h':image_h,
        }

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://creator.miaopai.com/upload',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        try:
            res = self.sess.post(publish_url,data = data,headers = headers)
            res_json = res.json()
            #print(res_json)
            ret = {
                'pub_ok':1 if res_json['data']['msg']=='OK' else 0,
                'msg':'视频发布成功！' if res_json['data']['msg']=='OK' else '视频发布失败！' + res_json['msg'] ,#+ self.file_name if res_json['data']['msg']=='OK' else '视频发布失败！' + res_json['msg']+ self.file_name,
                'channel':res_json['data']['channel'],
            }
            self.finsig.append('视频发布成功！')
            self.finishSignal.emit([1,self.finsig])

        except Exception as e:
            ret = {
                'pub_ok':0,
                'msg':'视频发布失败！' + self.file_name
            }

            msg = res_json['msg'] if 'res_json' in dir() else ''

            self.finsig.append('视频发布失败！' + msg)
            self.finishSignal.emit([0,self.finsig])
            return
        return ret
    def getlist(self):
        url_api = 'http://creator.miaopai.com/video/getList'
        data = {
            'page': '1',
            'count': '20',
        }
        try:
            res = self.sess.post(url_api, headers=self.headers, data=data)
            res_json = res.json()
            if res_json['data']['list']:
                return res_json['data']['list']

        except Exception as e:
            pass
        return res.json()

class loginThread(QThread):   #登陆线程，防止登陆时卡死
    loginSignal = pyqtSignal(list)  # [status=0,1,msg]

    def __init__(self, sess,ui,url, headers, data, conf,parent=None):
        super(loginThread, self).__init__(parent)

        self.sess = sess
        self.ui = ui
        self.headers = headers
        self.data = data
        self.conf = conf
        self.url = url


    def run(self):
        try:
            res = self.sess.post(self.url,headers = self.headers,data = self.data)
            json = res.json()
            code = json['code']
            msg = json['msg']

            if code == 200:
                isLogin = 1
                msg = '登陆成功'#,帐号：' + str(self.phone)
                self.ui.btn_login.setText('已登陆，断开')
                #self.ui.btn_getlist.setDisabled(False)
                self.ui.btn_login.setDisabled(False)
                cat_len = self.ui.category.count()
                if cat_len < 3:
                    self.addCategories()
                    if len(self.conf['sort_index']) > 0:
                        index = int(self.conf['sort_index'])
                        self.ui.category.setCurrentIndex(index)

            else:
                isLogin = 0
                msg = '登陆失败，信息：' + msg
                self.ui.btn_login.setText('登陆')
                self.ui.btn_login.setDisabled(False)

        except Exception as e:
            self.ui.btn_login.setText('登陆')
            self.ui.btn_login.setDisabled(False)
            self.ui.upload.setDisabled(True)
            print(e)
            isLogin = 0

            msg = '登陆失败，信息：网络不通或登陆接口变更' + str(e)
        self.ui.isLogin = isLogin
        self.ui.txtSignal.emit(['提示',msg])
        if isLogin == 1:
            self.t1 = getVideothread(self.sess,self.headers)
            self.t1.getListSignal.connect(self.ui.addList)
            self.t1.start()




        # return {'isLogin':isLogin,
        #           'msg':msg}
    def addCategories(self):
        url_api = 'http://creator.miaopai.com/video/getCategories'
        self.ui.category.removeItem(0)
        res_cat = self.sess.post(url_api,headers = self.headers)
        self.ui.l_cat = res_cat.json()['data']['result']
        n = 0
        for x in self.ui.l_cat:
            self.ui.category.insertItem(x['id'],x['name'])
        self.ui.category.setCurrentIndex(0)

class getVideothread(QThread):
    getListSignal = pyqtSignal(dict)
    getlistDisableSignal = pyqtSignal(int)
    def __init__(self,sess,headers):
        super().__init__()
        self.sess = sess
        self.headers = headers
    def run(self):
        count = 20
        url_api = 'http://creator.miaopai.com/video/getList'

        data = {
            'page': '1',
            'count': count
        }
        try:
            res = self.sess.post(url_api, data=data, headers=self.headers)
            json = res.json()
            dres = dict(json)
            n = 0
            for d in dres['data']['list']:
                url = d['cover']

                img = requests.get(url).content
                dres['data']['list'][n]['cover'] = img
                n += 1

            self.getListSignal.emit(dres)
            time.sleep(1.5)
            self.getlistDisableSignal.emit(0)

        except Exception as e:
            print(e)
            self.getlistDisableSignal.emit(1)
            return







