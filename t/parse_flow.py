import yaml
import os
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
domain_configs_rel_path = "../configs/domain_configs.yml"
domain_configs_file = os.path.join(script_dir, domain_configs_rel_path)




domain_configs = None
with open(domain_configs_file, mode='r',encoding='utf-8' ) as infile:
    domain_configs = yaml.safe_load(infile)
key_path = "a03.nodes.work.urls.work.parse"
parse = domain_configs["a03"]["nodes"]["work"]["urls"]["work"]["actions"]["parse"]

