# -*- coding:utf-8 -*-

# How to format data and replace templates is here
import os, logging
from tornado.template import Loader


g_tab = 0

class ToStringTemplate:
    def __init__(self):
        pass

    # Get parameter type.
    def getType(self, value):
        if isinstance(value, int):
            if isinstance(value, bool):
                return 'bool'
            return 'integer'
        elif isinstance(value, bytes):
            return 'bytes'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, list):
            return 'list'
        elif isinstance(value, dict):
            return 'dict'
        else:
            return 'Error Type:' + str(type(value))

    # Convert incoming arguments (int, bool, list, dict, etc.) to string.
    def toStr(self, key):
        key_type = self.getType(key)
        if key_type == 'bytes':
            return bytes.decode(key)
        elif key_type == 'string':
            return key
        elif key_type == 'integer':
            return str(key)
        elif key_type == 'bool':
            if key:
                return 'true'
            else:
                return 'false'
        elif key_type == 'list':
            return self.list2str(key)
        elif key_type == 'dict':
            return self.dict2str(key)
        else:
            return 'not know type Return!'

    # List to String
    # comment：is not mixed with a single element when stored in a dict list.
    def list2str(self, list_x):
        global g_tab
        buff = ''
        buff = buff + "["
        g_tab = g_tab + 1

        for value in list_x:
            value_type = self.getType(value)
            if value_type == 'dict':
                if list_x[0] == value:
                    if len(list_x) == 1:
                        buff = buff + self.dict2str(value)
                        buff = buff[:-2]
                    else:
                        buff = buff + "\n" + "\t" + self.dict2str(value)
                else:
                    if list_x[-1] == value:
                        buff = buff + "\t" + self.dict2str(value)
                        buff = buff[:-2] + "\n"
                    else:
                        buff = buff + "\t" + self.dict2str(value)
            elif value_type == 'list':
                buff = buff + self.list2str(value)
            else:
                if len(list_x) > 1:
                    if list_x[-1] != value:
                        buff = buff + "'" + self.toStr(value) + "', "
                    else:
                        buff = buff + "'" + self.toStr(value) + "'"
                else:
                    buff = buff + "'" + self.toStr(value) + "'"

        g_tab = g_tab - 1
        buff = buff + "]"
        return buff

    # Dict to String
    def dict2str(self, dict_x):
        global g_tab
        buff = ''

        g_tab = g_tab + 1
        tabs = self.getTabs()
        if len(dict_x) == 1:
            buff = buff + "{"
            for key in dict_x:
                buff = buff + "'" + self.toStr(key) + "': "

                value = dict_x[key]
                value_type = self.getType(value)
                if value_type == 'dict':
                    if list(dict_x)[-1] == key:
                        buff = buff + self.dict2str(value)
                        buff = buff[:-2]
                    else:
                        buff = buff + self.dict2str(value)
                elif value_type == 'list':
                    if list(dict_x)[-1] == key:
                        buff = buff + self.list2str(value) + "\n"
                    else:
                        buff = buff + self.list2str(value) + ",\n"
                elif value_type == 'integer':
                    buff = buff + self.toStr(value)
                elif value_type == 'bool':
                    buff = buff + self.toStr(value) + '\n'
                elif value_type == 'bytes':
                    buff = buff + self.toStr(value)
                else:
                    buff = buff + "'" + self.toStr(value) + "'"
        else:
            buff = buff + "{\n"

            for key in dict_x:
                buff = buff + tabs + '\t' + "'" + self.toStr(key) + "': "

                value = dict_x[key]
                value_type = self.getType(value)
                if value_type == 'dict':
                    if list(dict_x)[-1] == key:
                        buff = buff + self.dict2str(value)
                        buff = buff[:-2] + '\n'
                    else:
                        buff = buff + self.dict2str(value)
                elif value_type == 'list':
                    if list(dict_x)[-1] == key:
                        buff = buff + self.list2str(value) + "\n"
                    else:
                        buff = buff + self.list2str(value) + ",\n"
                elif value_type == 'integer':
                    buff = buff + self.toStr(value)
                elif value_type == 'bool':
                    buff = buff + self.toStr(value) + '\n'
                elif value_type == 'bytes':
                    buff = buff + self.toStr(value)
                else:
                    # if len(dict_x) > 1:
                    if list(dict_x)[-1] != key:
                        buff = buff + "'" + self.toStr(value) + "',\n"
                    else:
                        buff = buff + "'" + self.toStr(value) + "'\n"

        g_tab = g_tab - 1
        if g_tab > 0:
            buff = buff + tabs + "},\n"
            if len(dict_x) == 1:
                buff = buff.replace("\t", "")
        else:
            buff = buff + "}"
        return buff

    def getTabs(self):
        global g_tab
        buff = ''
        for i in range(g_tab - 1):
            buff = buff + '\t'
        return buff

    # Generate document content
    def generate_string(self, file_template, template_values, file_values):
        loader = Loader(os.path.join(os.getcwd(), 'templates'))
        ret = loader.load(file_template, parent_path='./')
        try:
            content = ret.generate().replace(template_values, file_values)
        except TypeError:
            logging.error("template_values or file_values is not bytes.")
            pass
        else:
            return content

    # Replaces the contents of the generated file with the contents of the corresponding file.
    def generate_file(self, file_name, file_template, template_values, file_values):
        content = self.generate_string(file_template, template_values, file_values)
        try:
            content_str = bytes.decode(content, encoding='utf-8')
        except TypeError:
            logging.error("descriptor 'decode' requires a 'bytes' object but received a 'NoneType'")
        else:
            cr_file = open(file_name, 'w', newline='\n')
            cr_file.write(content_str)
            cr_file.close()

    # two Generate document content
    def t_generate_string(self, file_template, template_values, file_values, template_values2, file_values2):
        loader = Loader(os.path.join(os.getcwd(), 'templates'))
        ret = loader.load(file_template, parent_path='./')
        try:
            content = ret.generate().replace(template_values, file_values).replace(template_values2, file_values2)
        except TypeError:
            logging.error("template_values or file_values is not bytes.")
            pass
        else:
            return content

    # Replaces the contents of the generated file with the contents of the corresponding file.
    def t_generate_file(self, file_name, file_template, template_values, file_values, template_values2, file_values2):
        content = self.t_generate_string(file_template, template_values, file_values, template_values2, file_values2)
        try:
            content_str = bytes.decode(content, encoding='utf-8')
        except TypeError:
            logging.error("descriptor 'decode' requires a 'bytes' object but received a 'NoneType'")
        else:
            cr_file = open(file_name, 'w', newline='\n')
            cr_file.write(content_str)
            cr_file.close()

    # three Generate document content
    def s_generate_string(self, file_template, template_values, file_values, template_values2,
                             file_values2, template_values3, file_values3):
        loader = Loader(os.path.join(os.getcwd(), 'templates'))
        ret = loader.load(file_template, parent_path='./')
        try:
            content = ret.generate().replace(template_values, file_values).\
                          replace(template_values2, file_values2).replace(template_values3, file_values3)
        except TypeError:
            logging.error("template_values or file_values is not bytes.")
            pass
        else:
            return content

    # Replaces the contents of the generated file with the contents of the corresponding file.
    def s_generate_file(self, file_name, file_template, template_values, file_values, template_values2,
                           file_values2, template_values3, file_values3):
        content = self.s_generate_string(file_template, template_values, file_values, template_values2,
                                         file_values2, template_values3, file_values3)
        try:
            content_str = bytes.decode(content, encoding='utf-8')
        except TypeError:
            logging.error("descriptor 'decode' requires a 'bytes' object but received a 'NoneType'")
        else:
            cr_file = open(file_name, 'w', newline='\n')
            cr_file.write(content_str)
            cr_file.close()
