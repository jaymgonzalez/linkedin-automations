import json
import logging
from app.services.scrapping_service import set_profile_rid, get_profile_json
from app.utils.data_utils import (
    create_columns,
    check_is_not_empty,
    get_urls,
    get_ids,
    append_item_to_row,
    remove_links_and_specific_key,
)
from app.services.openai_services import (
    synthesize_profile,
    create_connection_request_message,
)
from app.services.gsheets import sheet_to_df, df_to_sheet

logging.basicConfig(level=logging.INFO)


def update_csv_with_rid(sheet_name, column_name="linkedinUrl"):
    logging.info("Loading Sheet")
    df = sheet_to_df(sheet_name)

    create_columns(df, ["rid"])

    logging.info("Getting URLs")
    linkedin_urls = get_urls(df, column_name)

    logging.info(linkedin_urls)
    # linkedin_urls = linkedin_urls[2:]

    for url in linkedin_urls:

        if check_is_not_empty(df[df[column_name] == url].index[0], df, "rid"):
            continue
        else:
            logging.info(f"Getting rid for {url}")
            id = set_profile_rid(url)
            # the id in this case is the URL
            append_item_to_row(df, id, url, column_name, "rid")

    logging.info("Saving Sheet")
    df_to_sheet(df, sheet_name)


def update_csv_with_profile(sheet_name, column_name="rid"):
    logging.info("Loading Sheet")
    df = sheet_to_df(sheet_name)

    create_columns(
        df, ["linkedinProfile", "synthesizedProfile", "connectionRequestMessage"]
    )

    logging.info("Getting IDs")
    ids = get_ids(df, column_name)

    ids = ids[2:4]

    for id in ids:
        index = df[df[column_name] == id].index[0]

        if check_is_not_empty(index, df, "linkedinProfile"):
            continue

        logging.info(f"Getting profile for {id}")
        profile = get_profile_json(id)

        if profile is None:
            continue

        profile = json.loads(profile)

        df = append_item_to_row(df, profile, id, column_name, "linkedinProfile")

        profile = remove_links_and_specific_key(profile)

        profile = json.dumps(profile)

        if check_is_not_empty(index, df, "synthesizedProfile"):
            continue

        logging.info(f"Synthesizing profile for {id}")
        df = append_item_to_row(
            df, synthesize_profile(profile), id, column_name, "synthesizedProfile"
        )

        if check_is_not_empty(index, df, "connectionRequestMessage"):
            continue

        logging.info(f"Creating message for {id}")
        first_name = df.at[index, "firstName"]
        df = append_item_to_row(
            df,
            create_connection_request_message(profile, first_name),
            id,
            column_name,
            "connectionRequestMessage",
        )

    logging.info("Saving Sheet")
    df_to_sheet(df, sheet_name)


def create_new_message(sheet_name, index, column_name="synthesizedProfile"):
    df = sheet_to_df(sheet_name)

    profile = df.at[index, column_name]

    first_name = df.at[index, "firstName"]

    if profile is not None:
        try:
            message = create_connection_request_message(profile, first_name)
            print(message)

            df.at[index, "connectionRequestMessage"] = message

            df_to_sheet(df, sheet_name)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    # update_csv_with_rid("freelanceUK")
    update_csv_with_profile("freelanceUK")
    # create_new_message("freelanceUK", 1)
