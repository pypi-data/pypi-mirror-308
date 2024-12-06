import os
import subprocess
p1 = subprocess.run(['calc'], text=True)
print(p1.stdout)



