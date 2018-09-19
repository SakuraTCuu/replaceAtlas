# -*- coding: cp936 -*-
import json
def read_plist():
    plist_uuid = []
    str_plist = raw_input('请输入需要替换的图集plist文件：str_plist = ')
    #fo = open('FishKinds.plist.meta','r')
    fo = open(str_plist,'r')
    data = json.load(fo)
    atlas = data['uuid']
    for i in data['subMetas']:
               new_uuid = data['subMetas'][i]['uuid']
               plist_uuid.append({'name':i,'new_uuid':new_uuid,'atals_uuid':atlas})
    #print plist_uuid          
    fo.close()
    return plist_uuid;
#read_plist()
