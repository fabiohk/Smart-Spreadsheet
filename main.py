import pandas as pd
from pandasai import Agent
from pandasai.llm import BambooLLM
import os

from auto_parser import AutoParser

import typer

from utils import suppress_stderr
from typing_extensions import Annotated

def make_agent(dfs: list[pd.DataFrame], llm) -> Agent:
	return Agent(dfs, config={"llm": llm, "enforce_privacy": True})

'''
openai = OpenAI(api_token=os.getenv("OPENAI_API_TOKEN", default=""))
bamboo = BambooLLM(api_key=os.getenv("BAMBOO_API_KEY", default=""))

openai_agent = make_agent(t3, openai)
bamboo_agent = make_agent(t3, bamboo)
'''

app = typer.Typer()

suppress_stderr()

from enum import StrEnum

from llms.bamboo import make_bamboo_agent

class AvailableLLMs(StrEnum):
	BAMBOO = "bamboo"
	OPENAI = "openai"


@app.command()
def auto(
	file_path: Annotated[str, typer.Argument(help="The path to XLSX file to parse the tables")],
	llm: Annotated[AvailableLLMs, typer.Argument(help="The LLM you want to answer your questions")] = AvailableLLMs.BAMBOO
):
	print("Starting to parse the file...")
	parser = AutoParser()
	tables = parser.parse_xlsx(file_path)
	agent = make_bamboo_agent(tables)

	while True:
		question = typer.prompt("Ask me anything")
		answer = agent.chat(question)
		if "Unfortunately, I was not able to answer your question" in answer:
			print("Unfortunately, I was not able to answer your question.")
		else:
			print(answer)


@app.command()
def manual(file_path: str):
	pass

if __name__ == "__main__":
	app()