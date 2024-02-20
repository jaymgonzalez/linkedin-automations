import re
import pandas as pd


def get_urls(df, column_name):
    linkedin_urls = df[column_name]

    linkedin_urls = (
        linkedin_urls.dropna()
        .apply(lambda x: x if x.startswith("https://www.linkedin.com") else None)
        .dropna()
        .tolist()
    )

    return linkedin_urls


def get_ids(df, column_name):
    ids = df[column_name]

    ids = ids.dropna().tolist()

    return ids


def create_columns(df, columns):
    for column in columns:
        if column not in df.columns:
            df[column] = None

    return df


def check_is_not_empty(index, df, column_name):
    try:
        if column_name in df.columns:
            cell_value = df.at[index, column_name]
            return (
                pd.notna(cell_value) and cell_value != "" and not cell_value.isspace()
            )
        else:
            raise ValueError(f"{column_name} does not exist in df.columns")

    except ValueError as e:
        print(e)
        exit()

    except Exception as e:
        print(e)
        return False


def remove_links_and_specific_key(d, target_key="peopleAlsoViewed"):
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    for key in list(
        d.keys()
    ):  # Use list(d.keys()) to avoid RuntimeError during iteration
        if key == target_key:
            del d[key]  # Remove the specific key
            continue  # Skip further checks and continue with the next iteration
        if isinstance(d[key], dict):
            d[key] = remove_links_and_specific_key(d[key], target_key)
        elif isinstance(d[key], list):
            d[key] = [
                (
                    remove_links_and_specific_key(item, target_key)
                    if isinstance(item, dict)
                    else item
                )
                for item in d[key]
            ]
        elif isinstance(d[key], str) and url_pattern.search(d[key]):
            del d[key]  # Remove key if value is a URL
    return d


def append_item_to_row(df, item, id, column_id, column_name):
    df = create_columns(df, [column_name])
    index = df[df[column_id] == id].index
    if not index.empty:
        df.at[index[0], column_name] = item

    return df
