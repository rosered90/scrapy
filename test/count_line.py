# -*- coding:utf-8 -*-
# https://www.jianshu.com/p/ea827390b47a

import os
base_dir = 'C:\Users\Administrator\Desktop\ORC'
file_lists = []
whitelist = ['java', 'xml']


def get_file(base_dir):
	global file_lists
	for parent, dir_names, file_names in os.walk(base_dir):
		for filename in file_names:
			ext = filename.split('.')[-1]
			# 只统计指定的文件类型，略过一些log和cache文件
			if ext in whitelist:
				file_lists.append(os.path.join(parent, filename))


def count_line(fname):
	count = 0
	for file_line in open(fname).readlines():
		if file_line != '' and file_line != '\n':  # 过滤掉空行
			count += 1
	print fname + '----', count
	return count


if __name__ == '__main__' :
	get_file(base_dir)
	totalline = 0
	for filelist in file_lists:
		totalline = totalline + count_line(filelist)
	print 'total lines:', totalline

