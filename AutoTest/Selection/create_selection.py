# -*- coding: utf-8 -*-
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
formdir = os.path.dirname(os.getcwd())  # 获取上一级目录

def create_selection():
	selection = []
	for i in os.walk( formdir + '\scripts'):
		for fileName in i[2:3][0]:
			filePath = os.path.join(i[0],fileName)
			if(check_if_python(filePath)):
				selection.append(filePath)
	return selection

def check_if_python(fileName):
	if fileName.endswith('.py'):
		return True

def create_selection_file(selection):
	filePath = os.path.join(curPath,'all_scripts_selection.txt')
	file = open(filePath,'w',encoding= 'utf-8')
	for scriptPath in selection:
		file.write(scriptPath+'\n')
	file.close()

if __name__ == '__main__':
    selection = create_selection()
    create_selection_file(selection)