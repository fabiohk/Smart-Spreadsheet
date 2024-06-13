import pandas as pd
from pandasai import Agent

from enums import AvailableLLM

from .bamboo import make_bamboo_agent
from .openai import make_openai_agent


def make_agent(tables: list[pd.DataFrame], chosen_llm: AvailableLLM) -> Agent:
    match chosen_llm:
        case AvailableLLM.BAMBOO:
            return make_bamboo_agent(tables)
        case AvailableLLM.OPENAI:
            return make_openai_agent(tables)
        case _:
            raise Error(f"Unknown LLM: {chosen_llm}")
