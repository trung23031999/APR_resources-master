#!/usr/bin/python3
from os import listdir
from os.path import isdir
import xml.etree.ElementTree as ET
import json

def read_buggy_methods(parent_path): #function read_buggy_methods, paramater: parent_path
    with open(parent_path + "/buggy_methods.json") as f: #open file buggy_methods.json in b_version and save as f
        return json.loads(f.read()) #function return json as an array

        
for b_version in [d for d in listdir() if isdir(d)]: #list tat ca cac file va folder trong thu muc hien tai
    passing_tests = []
    j_buggy_methods = read_buggy_methods(b_version) #luu array du lieu cua buggy_methods.json vao bien
    for coverage_file in listdir(b_version + '/coverages'): #list tat ca cac file trong folder hien tai +/coverages
        words = coverage_file.split('_') #split ten file coverage voi ki tu ngan cach la _ (gom test_class va test_case)
        test_class = words[0] #lay test_class
        test_case = '_'.join(words[1:-1])  #lay cac phan tu trong array word, tra ve string ngan cach nhau boi '_' (testCloning_coverage)
        tree = ET.parse(b_version + '/coverages/' + coverage_file) #phan tich file xml thanh cay 
        root = tree.getroot() #lay phan tu goc cua cay
        packages = root.findall("packages/package")
        for x_package in packages: #duyet cac packages trong file xml
            for j_package in j_buggy_methods['packages']: #duyet packages trong file json
                if j_package['name'] == x_package.attrib['name']: #neu package name json = package name xml
                    classes = x_package.findall("classes/class") #thi find all class trong xml
                    for x_class in classes: #duyet tat ca cac class
                        for j_class in j_package['classes']: #duyet tat ca class trong xml
                            if j_class['name'] == x_class.attrib['name']: #neu class name json = class name xml
                                methods = x_class.findall('methods/method') #thi duyet tat cac method
                                for x_method in methods: #nhu tren
                                    for j_method in j_class['methods']: #nhu tren
                                        if x_method.attrib['name'] == j_method['name'] and x_method.attrib['signature'] == j_method['signature'] and float(x_method.attrib['line-rate']) > 0:
                                        #neu method name, signature giong nhau va line rate > 0
                                            if not test_class + "::" + test_case in passing_tests:
                                                passing_tests.append(test_class + "::" + test_case) #luu test_class::test_case vao passing test array
                                break
                    break
    with open(b_version + '/related_tests', 'w') as passing_tests_file:
        for test in passing_tests:
            passing_tests_file.write(test + '\n')