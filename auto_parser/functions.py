import pandas as pd


def remove_outer_nan_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_remove = []
    is_consecutive = True
    for i, col in enumerate(df.isna().all(axis=0)):
        if col and is_consecutive:
            columns_to_remove.append(i)
        else:
            break

    for i, col in reversed(list(enumerate(df.isna().all(axis=0)))):
        if col and is_consecutive:
            columns_to_remove.append(i)
        else:
            break

    return df.drop(df.columns[columns_to_remove], axis=1)


def remove_outer_nan_rows(df: pd.DataFrame) -> pd.DataFrame:
    rows_to_remove = []
    is_consecutive = True
    for i, row in enumerate(df.isna().all(axis=1)):
        if row and is_consecutive:
            rows_to_remove.append(i)
        else:
            break

    for i, row in reversed(list(enumerate(df.isna().all(axis=1)))):
        if row and is_consecutive:
            rows_to_remove.append(i)
        else:
            break

    return df.drop(df.index[rows_to_remove], axis=0).reset_index(drop=True)


def split_df_by_row(
    df: pd.DataFrame, start: int, end: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    new_table = df[start:end]
    splitted_df = pd.DataFrame(df.iloc[start:end, :]).reset_index(drop=True)
    new_df = pd.DataFrame(df.iloc[end + 1 :, :]).reset_index(drop=True)
    return splitted_df, new_df


def parse_tables_from_df_by_rows(df: pd.DataFrame) -> list[pd.DataFrame]:
    tables = []
    df = remove_outer_nan_rows(df)
    end_boundaries = df.index[df.isna().all(axis=1) == True].tolist()

    while len(end_boundaries) > 0:
        table, df = split_df_by_row(df, 0, end_boundaries[0])
        tables.append(table)
        df = remove_outer_nan_rows(df)
        end_boundaries = df.index[df.isna().all(axis=1) == True].tolist()

    tables.append(df)

    return tables


def split_df_by_column(
    df: pd.DataFrame, start: int, end: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    splitted_df = df.loc[:, start:end]
    splitted_df = pd.DataFrame(splitted_df)
    new_df = pd.DataFrame(df.loc[:, end + 1 :])
    return splitted_df, new_df


def parse_tables_from_df_by_columns(df: pd.DataFrame) -> list[pd.DataFrame]:
    tables = []
    df = remove_outer_nan_columns(df)
    df.columns = range(df.columns.size)
    end_boundaries = df.columns[df.isna().all(axis=0) == True].tolist()

    while len(end_boundaries) > 0:
        table, df = split_df_by_column(df, 0, end_boundaries[0])
        tables.append(table)
        df = remove_outer_nan_columns(df)
        df.columns = range(df.columns.size)
        end_boundaries = df.columns[df.isna().all(axis=0) == True].tolist()

    tables.append(df)

    return tables


def parse_tables_from_df(df: pd.DataFrame) -> list[pd.DataFrame]:
    tables_from_df = parse_tables_from_df_by_rows(df)

    new_tables = []
    for table in tables_from_df:
        tables_from_df = parse_tables_from_df_by_columns(table)
        new_tables.extend(tables_from_df)

    return merge_tables(new_tables)


def merge_consecutives_dfs(tables: list[pd.DataFrame]) -> list[pd.DataFrame]:
    merged_tables = []
    last_pass_has_merged_tables = False
    i = 0

    while i < len(tables) - 1:
        if len(tables[i].columns) == len(tables[i + 1].columns):
            merged_table = pd.concat([tables[i], tables[i + 1]], axis=0)
            last_pass_has_merged_tables = True
            i += 1
        elif len(tables[i].index) == len(tables[i + 1].index):
            tables[i + 1].columns = range(
                len(tables[i].columns),
                len(tables[i].columns) + len(tables[i + 1].columns),
            )
            merged_table = pd.concat([tables[i], tables[i + 1]], axis=1)
            last_pass_has_merged_tables = True
            i += 1
        else:
            merged_table = tables[i]
            last_pass_has_merged_tables = False

        merged_tables.append(merged_table.reset_index(drop=True))
        i += 1

    if i == len(tables) - 1:
        merged_tables.append(tables[-1])

    return merged_tables


def merge_tables(tables: list[pd.DataFrame]) -> list[pd.DataFrame]:
    previous_number_of_tables = len(tables)
    tables = merge_consecutives_dfs(tables)
    current_number_of_tables = len(tables)

    while previous_number_of_tables != current_number_of_tables:
        previous_number_of_tables = current_number_of_tables
        tables = merge_consecutives_dfs(tables)
        current_number_of_tables = len(tables)

    return clear_tables(tables)


def define_first_row_as_column(df):
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    return df


def clear_tables(tables):
    tables = [
        define_first_row_as_column(remove_outer_nan_rows(t)).fillna(0) for t in tables
    ]

    for table in tables:
        table.columns = [str(col) for col in table.columns]

    return tables
