# -*- coding: cp936 -*-
import os,sys
import json
#from read_png import read_png
import read_png
import read_dir
def read_prefab_scene():
    str_path = raw_input('请输入预制体或者场景存放的根路径：path = ')
    path = r'F:\develop\svn\client\Fish\assets'
    #prefab_name = raw_input('请输入需要替换的具体文件名字：prefab_name = ')
    list_name = []
    list_name = read_dir.listdir(path , list_name)
    png_uuid = read_png.read_png()
    for every_prefab in list_name:
        print '读取过的文件有:' + every_prefab
        #fo = open('FishKindsUI.prefab','r')
        #fo_r = open('FishKindUI_2.prefab','w')
        fo = open(every_prefab, 'r')
        data_prefab_scene = json.load(fo)
        fo.close()
        prefab_name = os.path.split(every_prefab)[1]
        fo_r = open(every_prefab , 'w')
        #fo_r = open(prefab_name, 'w')
        #fo = open(str_prefab + '/' + prefab_name,'r')
        #fo_r = open(prefab_name,'w')
        #data_prefab_scene = json.load(fo)
        #png_uuid = read_png.read_png()
        for i in data_prefab_scene:
            if i['__type__'] == "cc.Sprite" and ('_spriteFrame' in i) and i['_spriteFrame'] and ('__uuid__' in i['_spriteFrame']):
                #for i in prefab_uuid:
                    for j in png_uuid:
                        if i['_spriteFrame']['__uuid__'] == j['old_uuid']:
                            i['_spriteFrame']['__uuid__'] = j['new_uuid']
                            i['_atlas'] = j['atals_uuid']
        replace_uuid = json.dumps(data_prefab_scene, sort_keys=True, indent=4, separators=(',', ': '))
        #json.dump(data_prefab_scene,fo_r)
        #print data_prefab_scene
        fo_r.write(replace_uuid)
                #cur_uuid = i['_spriteFrame']['__uuid__']
                #cur_atlas = i['_atlas']
                #prefab_uuid.append({'cur_uuid':cur_uuid, 'cur_atlas':cur_atlas})
        #fo.close()
        fo_r.close()
    #return prefab_uuid
read_prefab_scene()
print '替换成功，请下面的目录下查看：' + path
#print '生成的新的文件所在的目录是：'+ os.getcwd()
