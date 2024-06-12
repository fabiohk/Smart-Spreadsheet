import pandas as pd
import typer
from pandasai import Agent


def main_loop(agent: Agent):
    continue_in_loop = True
    while continue_in_loop:
        question = typer.prompt("Ask me anything")
        answer = agent.chat(question)
        if "Unfortunately, I was not able to answer your question" in answer:
            print("Unfortunately, I was not able to answer your question.")
        else:
            print(answer)

        continue_in_loop = typer.confirm("Want to ask another question?")

    print("Bye!")


def export_to_json(dfs: list[pd.DataFrame]):
    should_serialize_dfs = typer.confirm("Do you want to export the tables to JSON?")

    if should_serialize_dfs:
        path_to_export = typer.prompt("What is the path you want to export the tables?")
        for i, df in enumerate(dfs, start=1):
            df.to_json(f"{path_to_export}/table_{i}.json")
