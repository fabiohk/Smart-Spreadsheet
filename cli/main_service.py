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