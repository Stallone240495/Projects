import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('your_file.csv')

# Get the column names
columns = df.columns

# Check if all column names are unique
if len(columns) == len(set(columns)):
    print("All column names are unique.")
else:
    print("Some column names are not unique.")