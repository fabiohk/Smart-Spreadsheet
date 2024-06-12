import pandas as pd
from pandasai import Agent
from pandasai.llm import BambooLLM
from .utils import create_agent
import os

def make_bamboo_agent(tables: list[pd.DataFrame]) -> Agent:
	bamboo = BambooLLM(api_key=os.getenv("BAMBOO_API_KEY", default=""))
	return create_agent(tables, bamboo)