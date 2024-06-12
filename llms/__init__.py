from enums import AvailableLLMs
from pandasai import Agent
import pandas as pd
from .bamboo import make_bamboo_agent
from .openai import make_openai_agent

def make_agent(tables: list[pd.DataFrame], chosen_llm: AvailableLLMs) -> Agent:
	match chosen_llm:
		case AvailableLLMs.BAMBOO:
			return make_bamboo_agent(tables)
		case AvailableLLMs.OPENAI:
			return make_openai_agent(tables)
		case _:
			raise Error(f"Unknown LLM: {chosen_llm}")