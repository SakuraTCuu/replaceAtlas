# -*- coding: utf-8 -*-
import os,sys
import json


def read_plist():
    plist_uuid = []
    str_plist = raw_input('请输入图集配置文件plist.meta文件：plist.meta = ')
    fo = open(str_plist,'r')
    data = json.load(fo)
    atlas = data['uuid']
    for i in data['subMetas']:
            new_uuid = data['subMetas'][i]['uuid']
            plist_uuid.append({'name':i,'new_uuid':new_uuid,'atlas_uuid':atlas})
    fo.close()
    return plist_uuid;


def read_png():
    str_png = raw_input('请输入项目中碎图的目录：png_dir = ')
    dirs = os.listdir(str_png)
    plist_uuid = read_plist()
    png_uuid = []
    # 获取需要替换的图片info
    for i in plist_uuid:
        for j in dirs:
            if i['name'] + '.meta' == j:
                # png.meta中的名字
                name =i['name'].replace('.png','',1)
                fo = open(str_png + '/' + j, 'r')
                data_png = json.load(fo)
                old_uuid = data_png['subMetas'][name]['uuid']
                png_uuid.append({'old_uuid':old_uuid, 'new_uuid':i['new_uuid'], 'atlas_uuid':i['atlas_uuid']})
                fo.close()
    return png_uuid


def listdir(path, list_name):
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                listdir(file_path, list_name)
            elif os.path.splitext(file_path)[1] == '.fire' or os.path.splitext(file_path)[1] == '.prefab':
                list_name.append(file_path)
        return list_name


def run():
        path = raw_input('请输入预制体或者场景存放的根目录：path = ')
        list_name = []
        list_name = listdir(path, list_name)
        png_uuid = read_png()
        for replaceFile in list_name:
            print '正在读取替换:' + replaceFile
            fo = open(replaceFile, 'r')
            replace_file_json_data = json.load(fo)
            fo.close()
            os.path.split(replaceFile)[1]
            replace_file_data = open(replaceFile , 'w')
            for i in replace_file_json_data:
                if i['__type__'] == "cc.Sprite" and ('_spriteFrame' in i) and i['_spriteFrame'] and ('__uuid__' in i['_spriteFrame']):
                        for j in png_uuid:
                            if i['_spriteFrame']['__uuid__'] == j['old_uuid']:
                                i['_spriteFrame']['__uuid__'] = j['new_uuid']
                                i['_atlas'] = j['atlas_uuid']
            replace_uuid = json.dumps(replace_file_json_data, sort_keys=True, indent=4, separators=(',', ': '))
            replace_file_data.write(replace_uuid)
            replace_file_data.close()
            print "文件" + replaceFile + "替换成功"
        return path


if __name__ == "__main__":
    path = run()
print '所有文件替换成功，请重新打开creator查看：' + path
#print '生成的新的文件所在的目录是：'+ os.getcwd()
