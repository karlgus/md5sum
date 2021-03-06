#!/usr/bin/python3

from collections import Counter
import concurrent
import concurrent.futures
import hashlib
import pathlib

def onlyFiles(startdir):
    return [x for x in pathlib.Path(startdir).rglob("*") if x.is_file()]

#def checkfile(filename):
def returnFileSum(filename):
    with open(filename,'r',errors='ignore') as file_to_check:
        data = file_to_check.read()
        md5_returned = hashlib.md5(data.encode('utf-8')).hexdigest()
        return md5_returned

def return_multiple_files(path_sum_dic):
    tmp =  Counter(path_sum_dic.values()) 
    tmplist = [x for x in tmp if tmp[x] > 1 ]
    tmpdic = {}

    for key,values in path_sum_dic.items():
        if values in tmplist:
            #print(key,values)
            tmpdic[key] = values

#    print(tmpdic)
    return tmpdic

def show_files(tmpdic):
    for key,values in tmpdic:
        print(key,values)

def main():
    start = onlyFiles('/etc')
    fileMd5Sums = [ ]
    path_sum_dic = { }
    duplicate = {}
    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        path_sum_dic = {executor.submit(returnFileSum,paths): paths for paths in start}
        for feature in concurrent.futures.as_completed(path_sum_dic):
            paths = path_sum_dic[feature]
            try:
                data = feature.result()
            except PermissionError:
                return
            except Exception as exc:
                print('%r generated an error %s' % (paths,exc))
            else:
                duplicate[paths] = data

    onlyDuplicates = return_multiple_files(duplicate)
    for key,values in onlyDuplicates.items():
        print(key,values)

if __name__ == '__main__':
    main()
