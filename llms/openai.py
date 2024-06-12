import os

import pandas as pd
from pandasai import Agent
from pandasai.llm import OpenAI

from .utils import create_agent


def make_openai_agent(tables: list[pd.DataFrame]) -> Agent:
    openai = OpenAI(api_token=os.getenv("OPENAI_API_TOKEN", default=""))
    return create_agent(tables, openai)
