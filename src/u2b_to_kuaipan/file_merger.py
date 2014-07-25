# encoding: utf-8
# created on 2014年7月25日
# filename: file_merger.py
# version: 1.0
# author: linyi1987@gmail.com

import os
import sys

def file_merger():
    file_list = []
    cwd = os.getcwd()
    for file_name in os.listdir(cwd):
        if file_name.endswith('.mp4'):
            file_list.append(file_name)
    file_list.sort()
    if file_list:
        filename = file_list[0].split('-')[0] + '.mp4'
    f = open(filename, 'wb')
    block_sz = 1024 * 512


    file_total_size = 0
    file_size_now = 0

    for file_part in file_list:
        file_total_size += os.path.getsize(file_part)
    for file_part in file_list:
        inf = open(file_part, 'rb')
        while True:
            
            buffer_block = inf.read(block_sz)
            if not buffer_block:
                break
            f.write(buffer_block)
            
            file_size_now += len(buffer_block)
            complete_percent = int(file_size_now*50.0/file_total_size)
            status = str(round(int(file_size_now)/1024.0/1024.0, 1)) + 'MB\t' + '[' + '>'*complete_percent \
                      + ' '*(50-complete_percent) + ']' + '  %3.2f%%' % (file_size_now*100.0/file_total_size)
            sys.stdout.write('\r'+status)
            sys.stdout.flush()
        inf.close()
        os.remove(file_part)
    sys.stdout.write('\n')
    f.close()

def main():
    file_merger()

if __name__ == '__main__':
    main()
