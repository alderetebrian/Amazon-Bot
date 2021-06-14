import re

nivel_1 = 'https://www.amazon.es/b?ie=UTF8&node=16247123031&ref_=sd_allcat_flb'
nivel_2 ='https://www.amazon.es/s?bbn=16247123031&rh=n%3A599364031%2Cn%3A16247123031%2Cn%3A902503031&dc&qid=1611818418&rnid=599365031&ref=lp_16247123031_nr_n_3'
nivel_3 ='https://www.amazon.es/s?i=stripbooks&bbn=16247123031&rh=n%3A599364031%2Cn%3A16247123031%2Cn%3A902503031%2Cn%3A902506031&dc&qid=1611818424&rnid=902503ni031&ref=sr_nr_n_3'
nivel_4 ='https://www.amazon.es/s?i=stripbooks&bbn=16247123031&rh=n%3A599364031%2Cn%3A16247123031%2Cn%3A902503031%2Cn%3A902506031%2Cn%3A4893780031&dc&qid=1611818450&rnid=902506031&ref=sr_nr_n_2'

if re.match("=[a-zA-Z0-9_.-]&", nivel_1):
    print('verdadero')