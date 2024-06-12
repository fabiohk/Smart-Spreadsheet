import typer
from manual_parser.types import TableInfo
from typing import Optional
from enums import AvailableLLM
from manual_parser import ManualParser
from llms import make_agent
from .main_service import main_loop

def ask_for_table_info(sheet_name: Optional[str] = None):
	if sheet_name:
		use_previous_sheet_name = typer.confirm(f"Should use the previous sheet name ({sheet_name})?")
		if not use_previous_sheet_name:
			sheet_name = None

	if not sheet_name:
		sheet_name = typer.prompt("What is the sheet the table is?")

	topleft_cell = typer.prompt("What is the top left cell the table is in?")
	num_rows = int(typer.prompt("How many rows the table have?"))
	num_cols = int(typer.prompt("How many columns the table have?"))
	return TableInfo(sheet_name, topleft_cell, num_rows, num_cols)

def manual_command(file_path: str, llm: AvailableLLM):
	print("I'll need to collect some information from the file...")
	tables_info = [ask_for_table_info()]
	last_sheet_name = tables_info[0].sheet_name
	has_another_table_to_add = typer.confirm("Do you have any other table to add?")

	while has_another_table_to_add:
		tables_info.append(ask_for_table_info(last_sheet_name))
		has_another_table_to_add = typer.confirm("Do you have any other table to add?")

	parser = ManualParser()
	tables = parser.parse_xlsx(file_path, tables_info)
	agent = make_agent(tables, llm)
	main_loop(agent)