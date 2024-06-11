
## Main Flow
# Receive spreadsheet files
# Read spreadsheet
# Drop columns entirely composed of NaN

# Identify boundaries

## For example 1 (only row boundaries)
'''
import pandas as pd

df = pd.read_excel("./tests/example_0.xlsx", header=None)
end_boundaries = df.index[df.isna().all(axis=1) == True].tolist()
tables = []

# Drop first rows with NaN

start_boundary = 0
for end_boundary in end_boundaries:
	new_table = df[start_boundary:end_boundary]
	headers = new_table.iloc[0]
	new_df  = pd.DataFrame(new_table.values[1:], columns=headers)
	new_df
	tables.append(new_df)
	start_boundary = end_boundary + 1
'''

## For example 2 (only column boundaries)
'''
df = tables[0]
end_boundaries = df.index[df.isna().all(axis=1) == True].tolist()

tables_col = []
start_boundary = 0
for end_boundary in end_boundaries:
	new_table = df.iloc[:,start_boundary:int(end_boundary)]
	new_table
	tables_col.append(new_table)
	start_boundary = int(end_boundary) + 1

def group_consecutive(test_list):
	result = []
    i = 0
    while i < len(test_list):
        j = i
        while j < len(test_list) - 1 and test_list[j+1] == test_list[j]+1:
            j += 1
        result.append((test_list[i], test_list[j]))
        i = j + 1
    return result

'''

# Prompt user with questions
# Receive the question and ask ChatGPT or any other AI model
# Show the answer

