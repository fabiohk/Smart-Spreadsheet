from dataclasses import dataclass

@dataclass
class TableInfo:
	sheet_name: str
	topleft_cell: str
	num_rows: int
	num_cols: int