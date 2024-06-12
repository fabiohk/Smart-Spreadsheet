import typer

from auto_parser import AutoParser
from enums import AvailableLLM
from llms import make_agent

from .main_service import export_to_json, main_loop


def auto_command(file_path: str, llm: AvailableLLM):
    print("Starting to parse the file...")
    parser = AutoParser()
    tables = parser.parse_xlsx(file_path)
    export_to_json(tables)
    agent = make_agent(tables, llm)
    main_loop(agent)
