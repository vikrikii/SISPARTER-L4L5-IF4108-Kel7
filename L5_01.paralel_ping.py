# import os, re dan threading
import os
import re
import threading

# import time
import time

# buat kelas ip_check
class ip_check(threading.Thread):
    
    # fungsi __init__; init untuk assign IP dan hasil respons = -1
    def __init__ (self,ip):
        super(ip_check, self).__init__()
        self.ip = ip
        self.response = -1
    
    # fungsi utama yang diekseskusi ketika thread berjalan
    def run(self):
        # lakukan ping dengan perintah ping -n (gunakan os.popen())
        ping = os.popen("ping -n 2 "+self.ip, "r")
        
        # loop forever
        while True:
            # baca hasil respon setiap baris
            line = ping.readline()
            
            # break jika tidak ada line lagi
            if not line: break
            
            # baca hasil per line dan temukan pola Received = x
            recv = regex.findall(line)
            
            # tampilkan hasilnya
            if recv:
                self.response = int(recv[0])
                print((self.ip + ": " + self.status()))
                
    # fungsi untuk mengetahui status; 0 = tidak ada respon, 1 = hidup tapi ada loss, 2 = hidup
    def status(self):
        # 0 = tidak ada respon
        if self.response==0:
            return "Tidak ada respon"
        # 1 = ada loss
        if self.response==1:
            return "Ada loss"
        # 2 = hidup
        if self.response==2:
            return "Hidup"
        # -1 = seharusnya tidak terjadi
        if self.response==3:
            return "Seharusnya tidak terjadi"
            
# buat regex untuk mengetahui isi dari r"Received = (\d)"
regex = re.compile(r"Received = (\d)")

# catat waktu awal
start = time.time()

# buat list untuk menampung hasil pengecekan
check_results = []

# lakukan ping untuk 20 host
for suffix in range(1,20):
    # tentukan IP host apa saja yang akan di ping
    iplist = [" 179.60.192.36","179.60.192.36","179.60.192.36","216.58.213.174","216.58.213.174","216.58.213.174","216.58.201.238"
    ,"216.58.201.238","216.58.201.238","192.168.137.1","179.60.192.36","179.60.192.36","179.60.192.36","216.58.213.174","216.58.213.174","216.58.213.174","216.58.201.238"
    ,"216.58.201.238","216.58.201.238","192.168.137.1"]
    
    # panggil thread untuk setiap IP
    t = ip_check(iplist[suffix])
    
    # masukkan setiap IP dalam list
    check_results.append(t)
    
    # jalankan thread
    t.start()

# untuk setiap IP yang ada di list
for el in check_results:
    
    # tunggu hingga thread selesai
    el.join()
    
    # dapatkan hasilnya

# catat waktu berakhir
end = time.time()

# tampilkan selisih waktu akhir dan awal
print("Selisih Waktu : ",end-start)
