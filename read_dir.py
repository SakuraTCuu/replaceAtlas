# -*- coding: cp936 -*-
import os,sys,json
#str_path = raw_input('请输入预制体或者场景存放的根路径：path = ')
#path = r'F:\develop\svn\client\Fish\assets'
#list_name = []
def  listdir( path , list_name):
	for file in os.listdir(path):
		file_path = os.path.join(path, file)
		if os.path.isdir(file_path):
			listdir(file_path, list_name)
		elif os.path.splitext(file_path)[1] == '.fire' or os.path.splitext(file_path)[1] == '.prefab':
			list_name.append(file_path)
	#print list_name
	return list_name
#listdir(path,list_name)
#new_path = os.path.split(list_name[0])[1]
#print os.path.split(list_name[0])[1]
#print new_path
#new_file = open(new_path, 'w')
#new_file.close()
#path_prefab = list_name[0]
#print path_prefab
#fo = open(path_prefab, 'r')
#data = json.load(fo)
#print data

