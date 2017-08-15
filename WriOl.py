# -*- coding:utf-8 -*-
import os
import os.path
import codecs
import sys, getopt

class WriOl(object):
    """docstring for WriOl"""
    def __init__(self):
        super(WriOl, self).__init__()
        self.srcCode = 'gbk'
        self.desCode = 'gbk'
        self.fliter = []

    def SrcFileCode(self, srcCode):
        self.srcCode = srcCode

    def DesFileCode(self, desCode):
        self.desCode = desCode

    def WritFile(self, rootdir, fileWrite):
        for parent, dirnames, filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:                        #输出文件信息
                if self.Filter(filename):
                    continue
                file = os.path.join(parent, filename)
                print "filename is:" + file
                file_object = codecs.open(file, 'r', self.srcCode)
                try:
                    lins = file_object.readlines()
                    file_write = codecs.open(fileWrite, 'a+', self.desCode)
                    try:
                        file_write.write(filename + '\r\n\r\n')
                        for line in lins:
                            if self.srcCode != self.desCode:
                                line = line.encode(self.desCode)
                            file_write.writelines(line)
                        file_write.write('\r\n\r\n\r\n')
                    finally:
                        file_write.close()
                finally:
                    file_object.close()

    def FilterOpt(self, filterfile):
        self.fliter = filterfile.split(',')

    def Filter(self, file):
        if self.fliter:
            Fix = os.path.splitext(file)[1]
            if Fix in self.fliter:
                return False
            return True
        return True

    def UserHelp(self):
        print "WriOl.exe -h"
        print "WriOl.exe --help"
        print "WriOl.exe -s srcDir -d desfile (-u srccode)(-e descode)(-f .cpp,.h)"
        print "WriOl.exe --srcdir srcDir --desfile desfile (--srccode srccode)(--descode descode)(--filter filterfile)"
        print "eg: WriOl.exe -s c:\\date -d c:\\des.txt or WriOl.exe -s c:\\date -d c:\\des.doc -u utf-8 -e utf-8"

def main():
    woi = WriOl()
    try:
        srcDir = ''
        desFile = ''
        # opts：一个列表，列表的每个元素为键值对  
        # args:其实就是sys.argv[1:]  
        # sys.argv[1:]：只处理第二个及以后的参数  
        # "ts:h"：选项的简写，有冒号的表示后面必须接这个选项的值（如 -s hello）  
        # ["help", "test1", "say"] :当然也可以详细地写出来，不过要两条横杠（--）
        opts, args = getopt.getopt(sys.argv[1:], "s:d:u:e:f:h", ["help", "srcdir", "desfile", "srccode", "descode", 'filter']) 

        # 具体处理命令行参数  
        for o, v in opts:  
            if o in ("-h","--help"):  
                woi.UserHelp()  
            elif o in ("-s", "--srcdir"):  
                srcDir = v
            elif o in ("-d", "--desfile"):  
                desFile = v
            elif o in ("-u", "--srccode"):  
                woi.SrcFileCode(v)
            elif o in ("-e", "--descode"):  
                woi.DesFileCode(v)
            elif o in ("-f", "--filter"):
                woi.FilterOpt(v)

        woi.WritFile(srcDir, desFile)

    except Exception, e:
        woi.UserHelp()
        raise e
    else:
        pass

if __name__ == '__main__':
    main()
    # AllFile('C:\\Users\\hasee\\Desktop\\source', 'C:\\Users\\hasee\\Desktop\\source.doc')
