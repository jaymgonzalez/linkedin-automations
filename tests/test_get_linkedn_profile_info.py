import pandas as pd
from main import check_if_exists

# Test case 1: column_name exists in df.columns and value is not NaN
df1 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
index1 = 0
column_name1 = "A"
assert check_if_exists(index1, df1, column_name1) == True

# Test case 2: column_name exists in df.columns but value is NaN
df2 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
index2 = 1
column_name2 = "B"
assert check_if_exists(index2, df2, column_name2) == True

# Test case 3: column_name does not exist in df.columns
df3 = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
index3 = 3
column_name3 = "C"
assert check_if_exists(index3, df3, column_name3) == False

# Test case 4: df is empty
df4 = pd.DataFrame()
index4 = 0
column_name4 = "A"
assert check_if_exists(index4, df4, column_name4) == False
