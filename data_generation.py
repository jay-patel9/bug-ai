# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:21:05 2020

@author: JAY
"""
import os
import subprocess
import pandas as pd
from bs4 import BeautifulSoup
from urllib import request
import re
import numpy as np

def get_all_code():
    resp = request.urlopen("http://pylint-messages.wikidot.com/all-messages")
    soup = BeautifulSoup(resp, 'lxml')
    
    link_test = []
    for link in soup.find_all('a', href=True):
        if link.text:
            link_test.append(link['href'])
    
    r = re.compile("^/messages:*")
    newlist = list(filter(r.match, link_test))
    
    codes = []
    prefix = '/messages'
    for i in newlist:
        i = i.strip(prefix)
        codes.append(i.upper()[1:])
    
    #print(codes)
    codes.append("code")
    codes.append("code_token")
    return codes


def get_codes():
    f = open('data_file/info.txt', 'r')
    tokens = f.readlines()
    all_codes = ['E0001', 'F0001', 'W0511', 'E0103', 'W1501', 'E1101', 'E1103', 'E0102', 'E1102', 'F0002', 'C0326', 'W0150', 'R0922', 'R0921', 'W0212', 'E0203', 'E0202', 'W1401', 'W1402', 'W0221', 'W0199', 'E1111', 'W1111', 'W0633', 'W0201', 'E0701', 'E1003', 'W0311', 'E0012', 'C0102', 'W0703', 'W0512', 'E0712', 'W0232', 'C0202', 'C0324', 'R0401', 'W0102', 'I0022', 'E0108', 'W0109', 'E1122', 'W0120', 'C0112', 'F0010', 'W0704', 'W0710', 'W0711', 'E1303', 'E0101', 'W0106', 'F0220', 'C0304', 'F0321', 'W1300', 'E1301', 'W0312', 'W0601', 'F0003', 'I0013', 'W0712', 'R0923', 'E0221', 'C0103', 'E0604', 'W0234', 'W0108', 'C0301', 'I0011', 'I0012', 'E1201', 'W0110', 'C0204', 'C0203', 'W0223', 'R0201', 'E0211', 'E0213', 'E1004', 'C0111', 'E1304', 'E1125', 'E0222', 'C0121', 'E1302', 'W0406', 'C0321', 'W0702', 'E0611', 'E0501', 'E1306', 'E1206', 'E0711', 'E1120', 'C1001', 'C0323', 'C0322', 'E1124', 'E1123', 'W0632', 'E0702', 'E0710', 'W0701', 'W0622', 'W0621', 'W0623', 'W0404', 'W0403', 'E0104', 'E0106', 'W0222', 'R0801', 'W1201', 'W0104', 'W0211', 'W0105', 'I0020', 'E1310', 'R0903', 'R0901', 'E1305', 'E1205', 'R0913', 'R0912', 'R0902', 'C0302', 'R0914', 'E1121', 'R0904', 'R0911', 'R0915', 'C0303', 'F0202', 'I0010', 'F0401', 'I0001', 'E0603', 'E0602', 'F0004', 'E0503', 'C0325', 'W0107', 'W0301', 'W0101', 'E0011', 'E1300', 'E1200', 'W0613', 'W0611', 'W0614', 'W1301', 'W0612', 'W0141', 'I0014', 'W0332', 'I0021', 'W1001', 'W0331', 'W0122', 'E0107', 'W0333', 'W0121', 'E1002', 'E1001', 'W0142', 'W0141', 'W0402', 'W0602', 'W0631', 'W0603', 'W0604', 'E0601', 'W0401', 'E0502', 'E0105', 'E0235', 'W0410', 'W0233', 'W0231', 'E0100', 'RP0002', 'RP0801', 'RP0401', 'RP0004', 'RP0003', 'RP0001', 'RP0402', 'RP0701', 'RP0101']

    try:
        codes = []
        for token in tokens:
            token = token.strip().split()
            codes.append(token[1].rstrip(':'))
    except:
        pass
    f.close()
    codes.pop(0)
    codes = [x for x in codes if x in all_codes]
    codes = list(set(codes))
    return codes


df = pd.read_json('python/final/jsonl/train/python_train_0.jsonl', lines=True)
code = df[['code', 'code_tokens']]
code = code.values.tolist()

all_codes = get_all_code()
all_codes = list(set(all_codes))
data = pd.DataFrame(columns=all_codes)

for i in range(len(code)):
    f = open("data_file/data.py", "w", encoding="utf-8")
    f.write(code[i][0])
    f.close()
    subprocess.run(["pylint", "data_file/data.py" ,">" ,"data_file/info.txt"], shell=True, cwd=os.getcwd())
    labels = []
    labels = get_codes()
    one_hot = list(np.ones(len(labels), dtype=int))
    labels.append('code')
    labels.append('code_token')
    one_hot.append(code[i][0])
    one_hot.append(code[i][1])
    temp_df = pd.DataFrame([one_hot], columns=labels)
    data = pd.concat([data,temp_df], axis=0)
    os.remove("data_file/data.py")
    os.remove("data_file/info.txt")
    
    
data.to_excel("dataset.xlsx")