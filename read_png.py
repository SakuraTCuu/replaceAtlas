# -*- coding: cp936 -*-
import json
import os
import sys
#from read_plist import read_plist
import read_plist
def read_png():
    str_png = raw_input('请输入存放相关图片的路径：str_png = ')
    #str_png_path = 'F:/develop/svn/client/Fish/assets/Texture/ui/FishKinds'
    #dirs = os.listdir(str_png_path)
    dirs = os.listdir(str_png)
    #str_path = raw_input('请输入图片meta的路径：')
    plist_uuid = read_plist.read_plist()
    #fo = open('fishTitle.png.meta', 'r')
    #data_png = json.load(fo)
    png_uuid = []
    for i in plist_uuid:
        for j in dirs:
        #fo = open(i['name']
            if i['name'] + '.meta' == j:
                #png.meta中的名字
                name =i['name'].replace('.png','',1)
                fo = open(str_png + '/' + j, 'r')
                data_png = json.load(fo)
                #old_uuid = data_png['subMetas']['fishTitle']['uuid']
                old_uuid = data_png['subMetas'][name]['uuid']
                png_uuid.append({'old_uuid':old_uuid, 'new_uuid':i['new_uuid'], 'atals_uuid':i['atals_uuid']})
                fo.close()
    #print png_uuid
    #fo.close()
    return png_uuid
#read_png()
