import numpy as np
import pandas as pd
import matplotlib

print("numpy版本:", np.__version__)
print("pandas版本:", pd.__version__)
print("matplotlib版本:", matplotlib.__version__)
arr = np.array([1,2,3,4,5])
print(arr.mean())