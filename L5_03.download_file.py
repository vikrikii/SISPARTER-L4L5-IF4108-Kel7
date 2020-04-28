#import os, request, threading, urllib.request, urllib.error, urllib.parse, dan time
import os
import requests
import threading
import urllib.request, urllib.error, urllib.parse
import time

#url awal
url = "https://apod.nasa.gov/apod/image/1901/LOmbradellaTerraFinazzi.jpg"

# Fungsi ini digunakan untuk membuat hitungan range
def buildRange(value, numsplits):
    lst = []
    #Lakukan perulangan sebanyak nilai dari parameter numsplits
    for i in range(numsplits):
        if i == 0:
            lst.append('%s-%s' % (i, int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
        else:
            lst.append('%s-%s' % (int(round(1 + i * value/(numsplits*1.0),0)), int(round(1 + i * value/(numsplits*1.0) + value/(numsplits*1.0)-1, 0))))
    return lst

#Buat class dengan nama SplitBufferThreads
class SplitBufferThreads(threading.Thread):
    """ Splits the buffer to ny number of threads
        thereby, concurrently downloading through
        ny number of threads.
    """
    # digunakan untuk init url dan hasil response
    def __init__(self, url, byteRange):
        super(SplitBufferThreads, self).__init__()
        self.__url = url
        self.__byteRange = byteRange
        self.req = None
        
    #fungsi utama yang akan dieksekusi ketika thread berjalan
    def run(self):
        # file yang didownload dalam ukuran byte
        self.req = urllib.request.Request(self.__url,  headers={'Range': 'bytes=%s' % self.__byteRange})
    
    #fungsi untuk membuka dan membaca file yang didownload
    def getFileData(self):
        #untuk membaca file
        return urllib.request.urlopen(self.req).read()

#main program,  
def main(url=None, splitBy=3):
    start_time = time.time()
    #untuk cek url valid apa tidak
    if not url:
        print("Please Enter some url to begin download.")
        return
    #variable berdasarkan data split dari hasil url
    fileName = url.split('/')[-1]
    #variable yg berisi besar data 
    sizeInBytes = requests.head(url, headers={'Accept-Encoding': 'identity'}).headers.get('content-length', None)
    #memberi keterangan jika terdapat download dan besaran data
    print("%s bytes to download." % sizeInBytes)
    #kondisi jika sizeinbytes false artinya tidak valid
    if not sizeInBytes:
        print("Size cannot be determined.")
        return
    #untuk menampung value
    dataLst = []
    # looping sebanyak nilai dari splitBY
    for idx in range(splitBy):
        #pecah data untuk looping dan dimasukan ke variable dataLst
        byteRange = buildRange(int(sizeInBytes), splitBy)[idx]
        bufTh = SplitBufferThreads(url, byteRange)
        bufTh.start()
        bufTh.join()
        #masukan data ke variable dataLst
        dataLst.append(bufTh.getFileData())
    # menggabungkan b dengan array dataList
    content = b''.join(dataLst)
    if dataLst:
        #hapus cache dari hasil download
        if os.path.exists(fileName):
            os.remove(fileName)
        print("--- %s seconds ---" % str(time.time() - start_time))
        #menulis data foto yg didownload  
        with open(fileName, 'wb') as fh:
            fh.write(content)
        print("Finished Writing file %s" % fileName)
		
#menjalankan fungsi main program
if __name__ == '__main__':
    main(url)
