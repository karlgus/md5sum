#!/usr/bin/python3

from collections import Counter
import glob
import getopt
import hashlib
import os


def onlyFiles(startdir):
    return [x for x in glob.glob(startdir+'**/*',recursive=True) if os.path.isfile(x)]

#def checkfile(filename):
def returnFileSum(filename):
    with open(filename,'r') as file_to_check:
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

    return tmpdic

def show_files(tmpdic):
    for key,values in tmpdic:
        print(key,values)

def main():

    start = onlyFiles('/srv/Data/')

    fileMd5Sums = [ ]
    path_sum_dic = { }
    for paths in start:
        #fileMd5Sums.append(returnFileSum(paths))
        path_sum_dic[paths] = returnFileSum(paths)
    
    duplicate =(return_multiple_files(path_sum_dic))
    for key,values in duplicate.items():
        print(key,values)

if __name__ == '__main__':
    main()
