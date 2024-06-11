import pandas as pd

## Main Flow
# Receive spreadsheet files
# Read spreadsheet
# Drop columns entirely composed of NaN

# Identify boundaries

## For example 1 (only row boundaries)
'''
import pandas as pd

df = pd.read_excel("./tests/example_0.xlsx", header=None)
end_boundaries = df.index[df.isna().all(axis=1) == True].tolist()[0]
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

def remove_outer_nan_columns(df):
	columns_to_remove = []
	is_consecutive = True
	for i, col in enumerate(df.columns.isna()):
		if col and is_consecutive:
			columns_to_remove.append(i)
		else:
			is_consecutive = False
	is_consecutive = True
	for i, col in reversed(list(enumerate(df.columns.isna()))):
		if col and is_consecutive:
			columns_to_remove.append(i)
		else:
			is_consecutive = False
	columns=columns_to_remove

'''
def remove_outer_nan_columns(df):
	columns_to_remove = []
	is_consecutive = True
	for i, col in enumerate(df.isna().all(axis=0)):
		if col and is_consecutive:
			columns_to_remove.append(i)
		else:
			break
	
	for i, col in reversed(list(enumerate(df.isna().all(axis=0)))):
		if col and is_consecutive:
			columns_to_remove.append(i)
		else:
			break
	
	return df.drop(df.columns[columns_to_remove], axis=1)

def remove_outer_nan_rows(df):
	rows_to_remove = []
	is_consecutive = True
	for i, row in enumerate(df.isna().all(axis=1)):
		if row and is_consecutive:
			rows_to_remove.append(i)
		else:
			break

	for i, row in reversed(list(enumerate(df.isna().all(axis=1)))):
		if row and is_consecutive:
			rows_to_remove.append(i)
		else:
			break

	return df.drop(df.index[rows_to_remove], axis=0)

def split_df(df, start, end):
	new_table = df[start:end]
	# headers = new_table.iloc[0]
	splitted_df = pd.DataFrame(df.iloc[start:end,:]).reset_index(drop=True)
	new_df = pd.DataFrame(df.iloc[end+1:,:]).reset_index(drop=True)
	return splitted_df, new_df


def split_df_into_tables(df):
	tables = []
	df = remove_outer_nan_rows(df)
	end_boundaries = df.index[df.isna().all(axis=1) == True].tolist()

	while len(end_boundaries) > 0:
		table, df = split_df(df, 0, end_boundaries[0])
		tables.append(table)
		df = remove_outer_nan_rows(df)
		end_boundaries = df.index[df.isna().all(axis=1) == True].tolist()

	tables.append(df)

	return tables

def split_df_by_column(df, start, end):
	splitted_df = df.iloc[:, start:end]
	splitted_df = pd.DataFrame(splitted_df)
	new_df = pd.DataFrame(df.iloc[:,end+1:])
	return splitted_df, new_df


def split_df_into_tables_by_columns(df):
	tables = []
	df = remove_outer_nan_columns(df)
	end_boundaries = df.columns[df.isna().all(axis=0) == True].tolist()

	while len(end_boundaries) > 0:
		table, df = split_df_by_column(df, 0, end_boundaries[0])
		tables.append(table)
		df = remove_outer_nan_columns(df)
		end_boundaries = df.columns[df.isna().all(axis=0) == True].tolist()

	tables.append(df)

	return tables

# Prompt user with questions
# Receive the question and ask ChatGPT or any other AI model
# Show the answer

def parse_xlsx(df, pass_loop):
	tables = [df]

	for _ in range(pass_loop):
		new_dfs = []
		for table in tables:
			tables_from_df = split_df_into_tables(table)
			new_dfs.extend(tables_from_df)
		dfs = []
		# len(new_dfs)
		for table_df in new_dfs:
			splitted_tables = split_df_into_tables_by_columns(table_df)
			dfs.extend(splitted_tables)
		tables = dfs

	return tables


'''
import pandas as pd
from main import split_df
from main import parse_xlsx

df = pd.read_excel("./tests/example_0.xlsx", header=None)
t1 = parse_xlsx(df, 1)

df = pd.read_excel("./tests/example_1.xlsx", header=None)
t2 = parse_xlsx(df, 1)

df = pd.read_excel("./tests/example_2.xlsx", header=None)
t3 = parse_xlsx(df, 1)

pass_loop = 2
tables = [df]

for i in range(pass_loop):
	for table in df:
		tables_from_df = split_df_into_tables(df)
		new_tables = []
		for table in tables:
			splitted_tables = split_df_into_tables_by_columns(table)
			new_tables.extend(splitted_tables)
'''