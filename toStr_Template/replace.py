# -*- coding:utf-8 -*-

import sys
import os, logging
sys.path.append(os.getcwd())
import argparse
from ToStr_Template import ToStringTemplate
# data template
from templates.data_template import d_examples_L, d_examples_D, d_examples
# replaced template
from templates.replaced_template import examples_L, examples_D, examples
# env variables and default parameters
from env.env import *


def replace_conf(vars):
    # Here's the custom method
    str_temp = ToStringTemplate()

    # environ: os.py defined dict. environ = {}
    env_dist = os.environ

    # connections: Get the default or in-environment configuration file parameters
    d_examples_L.append({'examples_1': vars['examples_1']})
    d_examples_L.append({'examples_2': vars['examples_2']})
    d_examples_L.append({'examples_3': vars['examples_3']})
    for conns in d_examples_L:
        # Template contains a required or tested element, Others can be added using add-ons
        if conns['examples'] == 'examples_value':
            conns['k1'] = vars['k1']
            conns['k2'] = vars['k2']
        elif conns['examples_1'] == vars['examples_1']:
            conns['v1'] = vars['v1']
            conns['v2'] = vars['v2']
            conns['v3'] = vars['v3']
        elif conns['examples_2'] == vars['examples_2']:
            conns['n1'] = vars['n1']
            conns['n2'] = vars['n2']
        elif conns['examples_3'] == vars['examples_3']:
            conns['s1'] = vars['s1']
            conns['s2'] = vars['s2']

    # variables: Get the default or in-environment configuration file parameters
    # Template contains a required or tested element, Others can be added using add-ons
    examples_D['examples'] = 'examples_value_replaced'
    examples_D['examples_k1'] = env_dist[vars_name['examples_k1']]
    examples_D['examples_k2'] = env_dist[vars_name['examples_k2']]

    # dags: Get the default list
    examples.append('examples', 'examples1', 'examples2')

    # Importing corresponding templates and convert format
    t_examples_L = str.encode(str_temp.list2str(d_examples_L))
    t_examples_D = str.encode(str_temp.dict2str(d_examples_D))
    t_examples = str.encode(str_temp.list2str(d_examples))

    # Configured parameters for format conversion
    r_examples_L = str.encode(str_temp.list2str(examples_L))
    r_examples_D = str.encode(str_temp.dict2str(examples_D))
    r_examples = str.encode(str_temp.list2str(examples))

    # Generate or modify the corresponding configuration file
    cnf_name = 'gen_con_file.py'
    str_temp.s_generate_file(cnf_name, 'replaced_template.py', t_examples_L, r_examples_L, t_examples_D, r_examples_D, t_examples, r_examples)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="select environment")
    parser.add_argument('-e', '--env', help="env: test/T dev/D staging/S production/P local/L", type=str, required=True)

    args = parser.parse_args()
    if args.env == 'test' or args.env == 'T':
        replace_conf(test)
    elif args.env == 'dev' or args.env == 'D':
        replace_conf(dev)
    elif args.env == 'staging' or args.env == 'S':
        replace_conf(staging)
    elif args.env == 'production' or args.env == 'P':
        replace_conf(production)
    elif args.env == 'local' or args.env == 'L':
        replace_conf(local)
    else:
        logging.error('Please select environment. (T: test; D: dev; S: staging; P: production; L: local)')
