### 模版替换方案

**注**：这里使用py脚本做配置文件，并在不同的环境中都可以生成或替换成环境所需要的py配置文件

1. 结构
.
├── Readme.md
├── ToStr_Template.py
├── __init__.py
├── env
│   ├── __init__.py
│   └── env.py
├── replace.py
└── templates
    ├── __init__.py
    ├── data_template.py
    └── replaced_template.py

2. 使用说明
  a. ToStr_Template.py 里面是数据格式化方法和模版替换方法
  b. replace.py 这可以看成一个使用例子
  c. templates 里包含里数据模版及替换输出的模版（主要是变量名和数据格式）
  d. env 下是环境变量名及默认参数，方便不同的环境统一提取配置数据及切换不同的环境

3. 文档中包含一个完整的例子
    ```shell
    python3 replace.py -e L
    ```
    在当前目录下会生成对应的配置文件：gen_con_file.py （脚本中有默认写成）
    之后就可以查看生成的文件数据，并正常调用里面的配置项
