# import mpi4py
from mpi4py import MPI

# import library random untuk generate angka integer secara random
import random

# buat COMM
COMM = MPI.COMM_WORLD

# dapatkan rank proses
rank = COMM.Get_rank()

# dapatkan total proses berjalan
size = COMM.Get_size()

# generate angka integer secara random untuk setiap proses
nilai = random.randint(0,100)
print ("Rank %d memiliki nilai = %d" %(rank, nilai))

# lakukam penjumlahan dengan teknik reduce, root reduce adalah proses dengan rank 0
sum = COMM.reduce(nilai, op=MPI.SUM, root=0)

# jika saya proses dengan rank 0 maka saya akan menampilkan hasilnya
if rank==0:
	print ("Rank 0 bekerja sebanyak = %d" %sum)