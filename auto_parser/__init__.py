import pandas as pd
from .functions import parse_tables_from_df

class AutoParser:
	def parse_xlsx(self, file_path: str) -> list[pd.DataFrame]:
		df = pd.read_excel(file_path, header=None)
		return parse_tables_from_df(df)