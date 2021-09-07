import numpy as np

A = np.array([[0.6667, -0.3333, -0.3333], [0.3333, -2.6667, 2.3333], [0.6667, -1.3333, 0.6667], [0, 0, 0]])
#print(A)
T = np.transpose(A)
#print(T)
print(A.dot(T))
print(T.dot(A))