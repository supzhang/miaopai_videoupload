def getList(self):
    url_api = 'http://creator.miaopai.com/video/getList'
    data = {
        'page': '1',
        'count': '99'
    }

    try:
        res = self.sess.post(url_api, data=data, headers=self.headers)
        json = res.json()

    except Exception as e:

        pass
    if json['code'] == 200:
        video_no = json['data']['total']
        self.allVideosNo.setText('本帐号共有视频个数：' + str(video_no))
        video_list = json['data']['list']
        # currentRow = self.okTable.currentRow()
        self.okTable.setRowCount(len(video_list))

        newRow = 0
        for v in video_list:
            # btnx = QPushButton("删除")
            # print(id(btnx))
            self.okTable.setRowHeight(newRow, 80)
            scid = v['scid']
            title = v['title']
            createtime = v['createtime']
            ftitle = v['desc']
            read = v['vcnt']
            txt = '<h4>' + title + '</h4>' + createtime + '<br/>' + '已看人数：' + str(read)
            item = QLabel(txt)
            self.okTable.setCellWidget(newRow, 0, item)
            self.okTable.setAlternatingRowColors(True)
            # self.okTable.setCellWidget(newRow,1,btnx)
            scid_item = QTableWidgetItem(scid)
            self.okTable.setItem(newRow, 2, scid_item)