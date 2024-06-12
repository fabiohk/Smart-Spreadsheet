import pandas as pd
from pandasai import Agent

## Main Flow
# Receive spreadsheet files
# Read spreadsheet

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

	return df.drop(df.index[rows_to_remove], axis=0).reset_index(drop=True)

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
	splitted_df = df.loc[:, start:end]
	splitted_df = pd.DataFrame(splitted_df)
	new_df = pd.DataFrame(df.loc[:,end+1:])
	return splitted_df, new_df


def split_df_into_tables_by_columns(df):
	tables = []
	df = remove_outer_nan_columns(df)
	df.columns = range(df.columns.size)
	end_boundaries = df.columns[df.isna().all(axis=0) == True].tolist()

	while len(end_boundaries) > 0:
		table, df = split_df_by_column(df, 0, end_boundaries[0])
		tables.append(table)
		df = remove_outer_nan_columns(df)
		df.columns = range(df.columns.size)
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
		for table_df in new_dfs:
			splitted_tables = split_df_into_tables_by_columns(table_df)
			dfs.extend(splitted_tables)
		tables = dfs

	return tables


def merge_consecutives_dfs(tables):
	merged_tables = []
	last_pass_has_merged_tables = False
	i = 0

	while i < len(tables) - 1:
		if len(tables[i].columns) == len(tables[i+1].columns):
			merged_table = pd.concat([tables[i], tables[i+1]], axis=0)
			last_pass_has_merged_tables = True
			i += 1
		elif len(tables[i].index) == len(tables[i+1].index):
			tables[i+1].columns = range(len(tables[i].columns), len(tables[i].columns) + len(tables[i+1].columns))
			merged_table = pd.concat([tables[i], tables[i+1]], axis=1)
			last_pass_has_merged_tables = True
			i += 1
		else:
			merged_table = tables[i]
			last_pass_has_merged_tables = False

		merged_tables.append(merged_table.reset_index(drop=True))
		i += 1

	if i == len(tables) - 1:
		merged_tables.append(tables[-1])

	return merged_tables

def merge_consecutives_dfs_column_priority(tables):
	merged_tables = []
	last_pass_has_merged_tables = False
	i = 0

	while i < len(tables) - 1:
		if len(tables[i].index) == len(tables[i+1].index):
			tables[i+1].columns = range(len(tables[i].columns), len(tables[i].columns) + len(tables[i+1].columns))
			merged_table = pd.concat([tables[i], tables[i+1]], axis=1)
			last_pass_has_merged_tables = True
			i += 1
		elif len(tables[i].columns) == len(tables[i+1].columns):
			merged_table = pd.concat([tables[i], tables[i+1]], axis=0)
			last_pass_has_merged_tables = True
			i += 1
		else:
			merged_table = tables[i]
			last_pass_has_merged_tables = False

		merged_tables.append(merged_table.reset_index(drop=True))
		i += 1

	if i == len(tables) - 1:
		merged_tables.append(tables[-1])

	return merged_tables


def merge_tables(tables):
	previous_number_of_tables = len(tables)
	tables = merge_consecutives_dfs(tables)
	current_number_of_tables = len(tables)

	while previous_number_of_tables != current_number_of_tables:
		previous_number_of_tables = current_number_of_tables
		tables = merge_consecutives_dfs(tables)
		current_number_of_tables = len(tables)

	return tables


def merge_tables_column_priority(tables):
	previous_number_of_tables = len(tables)
	tables = merge_consecutives_dfs_column_priority(tables)
	current_number_of_tables = len(tables)

	while previous_number_of_tables != current_number_of_tables:
		previous_number_of_tables = current_number_of_tables
		tables = merge_consecutives_dfs_column_priority(tables)
		current_number_of_tables = len(tables)

	return tables

def convert_columns(df):
	df.columns = [str(col) for col in df.columns]

def define_first_row_as_column(df):
	new_header = df.iloc[0]
	df = df[1:]
	df.columns = new_header
	return df


def make_agent(dfs, llm):
	return Agent(dfs, config={"llm": llm, "enforce_privacy": True})


def clear_tables(tables):
	tables = [define_first_row_as_column(remove_outer_nan_rows(t)).fillna(0) for t in tables]

	for t in tables:
		convert_columns(t)

	return tables

'''
import pandas as pd
from main import split_df
from main import parse_xlsx
from main import merge_consecutives_dfs
from main import merge_tables
from main import split_df_into_tables
from main import split_df_into_tables_by_columns
from main import remove_outer_nan_columns
from main import remove_outer_nan_rows
from main import merge_consecutives_dfs_column_priority
from main import merge_tables_column_priority
from main import convert_columns
from main import define_first_row_as_column
from main import clear_tables
import os
from pandasai import Agent
from pandasai.llm import BambooLLM
from pandasai.llm import OpenAI

openai = OpenAI(api_token=os.getenv("OPENAI_API_TOKEN", default=""))
bamboo = BambooLLM(api_key=os.getenv("BAMBOO_API_KEY", default=""))

df = pd.read_excel("./tests/example_0.xlsx", header=None)
t1 = parse_xlsx(df, 1)
t1 = merge_tables(t1)
t1 = clear_tables(t1)

openai_agent = make_agent(t1, openai)
bamboo_agent = make_agent(t1, bamboo)

df = pd.read_excel("./tests/example_1.xlsx", header=None)
t2 = parse_xlsx(df, 1)
t2 = merge_tables(t2)
t2 = clear_tables(t2)

openai_agent = make_agent(t2, openai)
bamboo_agent = make_agent(t2, bamboo)


df = pd.read_excel("./tests/example_2.xlsx", header=None)
t3 = parse_xlsx(df, 1)
t3 = merge_tables(t3)
t3 = clear_tables(t3)

openai_agent = make_agent(t3, openai)
bamboo_agent = make_agent(t3, bamboo)
'''