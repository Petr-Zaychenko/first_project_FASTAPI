from datetime import datetime, date
import os

res = str(date.today())
res_p = os.path.abspath("downloaded_files/1_а чё так можно было.png")

print(res)
print(res_p)
print(type(res))
print(type(res_p))
