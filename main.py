import pandas as pd
from pandasai import Agent
from pandasai.llm import BambooLLM
import os

from auto_parser import AutoParser

import typer

def make_agent(dfs: list[pd.DataFrame], llm) -> Agent:
	return Agent(dfs, config={"llm": llm, "enforce_privacy": True})

'''
openai = OpenAI(api_token=os.getenv("OPENAI_API_TOKEN", default=""))
bamboo = BambooLLM(api_key=os.getenv("BAMBOO_API_KEY", default=""))

openai_agent = make_agent(t3, openai)
bamboo_agent = make_agent(t3, bamboo)
'''

app = typer.Typer()

import sys

# sys.tracebacklimit = 0

def nothing(*args):
	pass

sys.stderr.write = nothing

@app.command()
def auto(file_path: str):
	print("Starting to parse the file...")
	parser = AutoParser()
	tables = parser.parse_xlsx(file_path)
	bamboo = BambooLLM(api_key=os.getenv("BAMBOO_API_KEY", default=""))
	agent = make_agent(tables, bamboo)
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