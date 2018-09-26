# -*- coding: utf-8 -*-
import os,sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

#图集文件的目录
str_plist = ""

#碎图的九宫格信息
png_border = []

'''
替换文件中的uuid 完全匹配替换
'''


def replace_file_uuid(replaceFile,png_uuid):
    with open(replaceFile,"r") as f:
        readlines = f.readlines()

    with open(replaceFile,"w+") as f_w:
        for line in readlines:
            for item in png_uuid:
                if item['old_uuid'] in line:
                    line = "\"__uuid__\":"+"\""+item['new_uuid']+"\""
                f_w.write(line)
    print "Modify File " + replaceFile + " success "

'''
写入图片的九宫格信息
TODO  重新设计
'''


def write_plist():
    global str_plist  # global声明
    plist_file_r = open(str_plist, 'r')
    plist_info = json.load(plist_file_r)
    plist_file_r.close()

    plist_file_w = open(str_plist, 'w')
    for i in plist_info['subMetas']:
            for j in png_border:
                if(i == j['imgName']):
                      ##写入九宫格信息
                        plist_info['subMetas'][i]['borderTop'] = j['border'][0]
                        plist_info['subMetas'][i]['borderBottom'] = j['border'][1]
                        plist_info['subMetas'][i]['borderLeft'] = j['border'][2]
                        plist_info['subMetas'][i]['borderRight'] = j['border'][3]
                        print j['imgName'] + "九宫格替换成功"

    newplist = json.dumps(plist_info, sort_keys=True, indent=4, separators=(',', ': '))
    plist_file_w.write(newplist)
    plist_file_w.close()
    print "=====九宫格替换完成====="


def read_plist():
    global str_plist # global声明
    plist_uuid = []
    str_plist = raw_input('请输入图集配置文件plist.meta文件：plist.meta = ')
    fo = open(str_plist,'r')
    data = json.load(fo)
    atlas = data['uuid']
    for i in data['subMetas']:
            new_uuid = data['subMetas'][i]['uuid']
            plist_uuid.append({'name':i,'new_uuid':new_uuid,'atlas_uuid':atlas})
    fo.close()
    return plist_uuid


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
                datainfo = data_png['subMetas'][name]
                old_uuid = datainfo['uuid']
                ##保存碎图的九宫格信息
                border = [datainfo['borderTop'], datainfo['borderBottom'], datainfo['borderLeft'], datainfo['borderRight']]

                if(border[0] != 0
                        or border[1] != 0
                        or border[2] != 0
                        or border[3] != 0):
                    # 需要写入到图集的meta文件里去  同步一下
                    # write_plist(i['name'], border)
                    png_border.append({'imgName': i['name'], 'border': border})

                png_uuid.append({'old_uuid': old_uuid, 'new_uuid': i['new_uuid'], 'atlas_uuid': i['atlas_uuid']})
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
            print '正在读取:' + replaceFile
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

            #开始替换其他脚本引用图片
            replace_file_uuid(replaceFile,png_uuid)
        #开始替换九宫格信息
        print "=====开始替换图片九宫格信息====="
        write_plist()
        return path


if __name__ == "__main__":
    path = run()
    print '所有文件替换成功，请重新打开creator查看：' + path
