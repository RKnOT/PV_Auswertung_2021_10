
import numpy as np

x = np.linspace(0,100,201)
y = np.random.random(201)

with open('BD_data.txt', 'w') as f:
    for i in range(len(x)):
        f.write('{:4.1f} {:.4f}\n'.format(x[i], y[i]))
        
        
with open('BD_data.txt', 'r') as f:
    data = f.read()

print(x)
print(y)
print(data)