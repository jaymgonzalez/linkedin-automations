import json
import pandas as pd
from app.services.scrapping_service import set_profile_rid, get_profile_json
from app.utils.data_utils import (
    create_columns,
    check_if_exists,
    get_urls,
    get_ids,
    append_item_to_row,
    remove_links_and_specific_key,
)
from app.services.openai_services import (
    synthesize_profile,
    create_connection_request_message,
)


def update_csv_with_rid(csv_name, column_name="linkedinUrl"):
    df = pd.read_csv(csv_name)

    create_columns(df, ["rid"])

    linkedin_urls = get_urls(df, column_name)

    linkedin_urls = linkedin_urls[2:5]

    for url in linkedin_urls:

        if check_if_exists(df[df[column_name] == url].index[0], df, "rid"):
            continue
        else:

            id = set_profile_rid(url)
            # the id in this case is the URL
            append_item_to_row(df, id, url, column_name, "rid")

    df.to_csv(csv_name, index=False)


def update_csv_with_profile(csv_name, column_name="rid"):
    df = pd.read_csv(csv_name)

    ids = get_ids(df, column_name)

    for id in ids:
        index = df[df[column_name] == id].index[0]

        if check_if_exists(index, df, "linkedinProfile"):
            continue

        profile = get_profile_json(id)

        if profile is None:
            continue

        profile = json.loads(profile)

        df = append_item_to_row(df, profile, id, column_name, "linkedinProfile")

        profile = remove_links_and_specific_key(profile)

        profile = json.dumps(profile)

        if check_if_exists(index, df, "synthesizedProfile"):
            continue

        df = append_item_to_row(
            df, synthesize_profile(profile), id, column_name, "synthesizedProfile"
        )

        if check_if_exists(index, df, "connectionRequestMessage"):
            continue

        df = append_item_to_row(
            df,
            create_connection_request_message(profile),
            id,
            column_name,
            "connectionRequestMessage",
        )

    df.to_csv(csv_name, index=False)


def create_new_message(csv_name, index, column_name="synthesizedProfile"):
    df = pd.read_csv(csv_name)

    profile = df.at[index, column_name]

    if profile is not None:
        try:
            message = create_connection_request_message(profile)
            print(message)

            df.at[index, "connectionRequestMessage"] = message

            df.to_csv(csv_name, index=False)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    # update_csv_with_rid("freelanceSpain.csv")
    # update_csv_with_profile("freelanceSpain.csv")
    create_new_message("freelanceSpain.csv", 2)
