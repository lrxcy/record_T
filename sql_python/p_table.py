# -*- coding: UTF-8 -*-

def print_table(two_dimension_list):
    '''
    打印表格函数
    输入一个2维列表,格式参见:
    [
    ["123,"123,"123"],
    ["123,"123","123]
    ...
    ]
    空行表示方法:
    ["","",""]
    注意每行的元素数需要相等
    :param two_dimension_list:
    :return:
    '''

    def sum_string_length(keys):
        length = 0
        for key in keys:
            if u'\u4e00' <= key <= u'\u9fff':
                length += 2
            elif u'\uFF01' <= key <= u'\uFF5E':
                length += 2
            else:
                length += 1
        return length

    four_space = " "
    # 列表元素为每一列最长字符的长度, 列表长度等于每一行的元素数
    each_col_max_length_list = []
    # 一行的元素个数
    row_element_count = len(two_dimension_list[0])
    for col in range(row_element_count):
        max_length = 0
        for i in range(len(two_dimension_list)):
            element_length = sum_string_length(two_dimension_list[i][col])
            if max_length < element_length:
                max_length = element_length
        each_col_max_length_list.append(max_length)
    # print('n: ', each_col_max_length_list)

    # 这个可以表示"|"的数量
    vertical_line_count = len(each_col_max_length_list)
    case_str = ""
    for i in range(vertical_line_count):
        n = each_col_max_length_list[i]
        case_str = case_str + "+{0}".format("-" * (n + 2))
    print(case_str + "+")

    for row_num in range(len(two_dimension_list)):
        output_str = "|"
        for element in range(len(two_dimension_list[row_num])):
            later_space_count = each_col_max_length_list[element] - sum_string_length(
                two_dimension_list[row_num][element]) + 1
            # 减一表示"|"占用一个空格位置
            space1 = " " * (later_space_count)
            output_str += "{space0}{value}{space1}|".format(space0=four_space,
                                                            value=two_dimension_list[row_num][element],
                                                            space1=space1)
        # 判断是否空行
        if output_str.replace("|", "").replace(" ", ""):
            print(output_str)
            if row_num == 0:
                print(case_str + "+")
        else:
            # 如果是空行
            output_str = "|"
            for i in range(len(two_dimension_list[row_num])):
                output_str += "-" * (each_col_max_length_list[i] + 2) + "|"
            output_str = output_str[:-1] + "|"
            output_str = output_str.replace('-', ' ')
            print(output_str)
    print(case_str + "+")


def main():
    test_list = [
        ["name", "code", "new"],
        ["", "", ""],
        ["Lorenzo", "123456789123456ASDAS3", "男"],
        ["Bianca", "", "女"],
        ["Laura", "123456789123456123123", "未知"]
    ]
    print_table(test_list)


if __name__ == "__main__":
    main()
