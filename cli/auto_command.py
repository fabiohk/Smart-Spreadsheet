import typer
from enums import AvailableLLM
from llms import make_agent
from .main_service import main_loop
from auto_parser import AutoParser

def auto_command(file_path: str, llm: AvailableLLM):
	print("Starting to parse the file...")
	parser = AutoParser()
	tables = parser.parse_xlsx(file_path)
	agent = make_agent(tables, llm)
	main_loop(agent)