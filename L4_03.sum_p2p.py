# import mpi4py
from mpi4py import MPI

# import library random untuk generate angka integer secara random
import random

# buat COMM
COMM = MPI.COMM_WORLD

# dapatkan rank proses
rank=COMM.Get_rank()

# dapatkan total proses berjalan
size=COMM.Get_size()

# generate angka integer secara random untuk setiap proses
nilai = random.randint(0,100)
print ("Rank %d memiliki nilai = %d" %(rank, nilai))

# jika saya adalah proses dengan rank 0 maka:
# saya menerima nilai dari proses 1 s.d proses dengan rank terbesar
# menjumlah semua nilai yang didapat (termasuk nilai proses saya)
if rank == 0:
	sum = nilai
	for i in range(1,size):
		sum += COMM.recv(source=i)
	print ("Rank 0 bekerja sebanyak= %d" %(sum))

# jika bukan proses dengan rank 0, saya akan mengirimkan nilai proses saya ke proses dengan rank=0
else:
	COMM.send(nilai, dest=0)