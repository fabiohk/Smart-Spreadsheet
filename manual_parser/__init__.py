import pandas as pd
from .functions import pick_table
from .types import TableInfo
from openpyxl import load_workbook

class ManualParser:
	def parse_xlsx(self, file_path: str, tables_list: list[TableInfo]) -> list[pd.DataFrame]:
		wb = load_workbook(file_path, data_only=True)
		return [pick_table(wb[table_info.sheet_name], table_info) for table_info in tables_list]
		
