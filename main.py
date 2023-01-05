from day_09 import part1_animated as part
import time


print(part.__name__, "\n")

ts = time.time()
result = part.run()
te = time.time()

print(f"time:{te-ts:.3}")
print ("result:", result)
