from pandasai import Agent
from pandasai.llm import LLM
import pandas as pd

def create_agent(dfs: list[pd.DataFrame], llm: LLM) -> Agent:
	return Agent(dfs, config={"llm": llm, "enforce_privacy": True})