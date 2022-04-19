#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# By Chen

import os, sys


def get_file_list(directory):
    """单独一个目录"""
    files_path_list = []
    files_p_list = []

    if os.path.exists(directory):
        directory_n = directory
    else:
        print ("%s 不是一个有效的目录！！！" % directory)
        sys.exit ()

    # 遍历目录下读取可读文件
    all_files_directory = os.walk(directory_n, topdown=True, followlinks=True)
    for root, dirs, files in all_files_directory:
        # 获取文件路径
        for f_name in files:
            if ".docx" in f_name:
                # print(f_name)
                file_path_d = os.path.join(root, f_name)
                file_path_m = os.path.join(root, f_name.replace(".docx", ".md"))
                files_path_list.append(file_path_d)
                files_p_list.append(file_path_m)

    return files_path_list, files_p_list

def convert_md(docx2md_cmd, f_docx, f_md, curr_path):
    
    cmd = "cd {} && {} {} > {}".format(curr_path.replace(' ','\ '), docx2md_cmd, f_docx.replace(' ','\ ').replace('(','\(').replace(')','\)'), f_md.replace(' ','-').replace('(','\(').replace(')','\)'))
    print(cmd)
    os.system(cmd) 

    img_cmd = "cd {} && if [ -d media ]; then mv media {}; fi".format(curr_path.replace(' ','\ '), f_md.replace(' ','-').replace('.md', 'img').replace('(','\(').replace(')','\)'))
    os.system(img_cmd) 

def main(docx2md_cmd, docs_path):
    fpl_docx, fpl_md = get_file_list(docs_path)
    print ('🚀-----------------起飞------------------🚀')
    for fpl_d in fpl_docx:
        progress = '{:.2f}%'.format(((fpl_docx.index(fpl_d) + 1) / len(fpl_docx)) * 100)
        # print(fpl_d,fpl_md[fpl_docx.index(fpl_d)])
        fpl_d_n = str(fpl_d.split('/')[-1])
        fpl_md_n = str(fpl_md[fpl_docx.index(fpl_d)].split('/')[-1])
        # print(fpl_d_n)
        # print(fpl_d_n)
        # print(str(fpl_d).rsplit('/', 1)[0])
        curr_path = str(fpl_d).rsplit('/', 1)[0]
        convert_md(docx2md_cmd, fpl_d_n, fpl_md_n, curr_path.replace('(','\(').replace(')','\)').replace('&','\&'))
        print('✈ 进度：{} ------  {}  ->>>--->>> 转换完成!'.format(progress, str(fpl_d.split('/')[-1])))


if __name__ == '__main__':
    docx2md_cmd = 'docx2md'
    linux_dir = "/data/tomd/test"
    main(docx2md_cmd, linux_dir)
    
