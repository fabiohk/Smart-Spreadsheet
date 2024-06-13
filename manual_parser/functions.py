import pandas as pd
from openpyxl.worksheet.worksheet import Worksheet

from .types import TableInfo


def pick_table(sheet: Worksheet, table_info: TableInfo) -> pd.DataFrame:
    topleft, num_rows, num_columns = (
        table_info.topleft_cell,
        table_info.num_rows,
        table_info.num_cols,
    )
    topleft_cell = sheet[topleft]

    header = pick_content_from_one_row(
        sheet, topleft_cell.row, topleft_cell.column, num_columns
    )
    content = [
        pick_content_from_one_row(
            sheet, topleft_cell.row + i, topleft_cell.column, num_columns
        )
        for i in range(1, num_rows)
    ]

    df = pd.DataFrame(content, columns=header)
    df = clear_nan_columns(clear_nan_rows(df))
    df.columns = [str(col) for col in df.columns]
    return df


def pick_content_from_one_row(
    sheet: Worksheet, row_index: int, start_column_index: int, num_columns: int
) -> list:
    return [
        sheet.cell(row_index, start_column_index + i).value for i in range(num_columns)
    ]


def clear_nan_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.isna().all(axis=1) == False].reset_index(drop=True)


def clear_nan_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:, df.isna().all(axis=0) == False]
