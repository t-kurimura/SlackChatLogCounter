import csv
import slack

token = "{token}"
oldest_ts = 1562405642
latest_ts = 1578306643
channel_id = "{channel_id}"
search_word = "{keyword}"


def _get_filtered_ts_list(search_keyword, message_list):
    ts_list = []
    for item in message_list:
        if item["text"] != "":
            break

        if item["subtype"] != "bot_message":
            break

        if item.get("icons") is None:
            break

        if item["icons"].get("emoji") != ":cry:":
            break

        if search_keyword not in item["attachments"][0]["fallback"]:
            break

        ts_list.append(int(float(item["ts"])))

    return ts_list


def _out_to_csv(input_list):
    with open("./output.csv", "x") as f:
        writer = csv.writer(f)
        for item in input_list:
            writer.writerow([item])


def exec_all():
    client = slack.WebClient(token=token)

    cursor = None
    target_message_ts_list = []

    current_latest_ts = latest_ts

    while current_latest_ts > oldest_ts:
        response = None
        if cursor is None:
            response = client.conversations_history(
                channel=channel_id, inclusive=1, latest=latest_ts
            )
        else:
            response = client.conversations_history(
                channel=channel_id, inclusive=1, latest=latest_ts, cursor=cursor
            )

        current_ts_list = _get_filtered_ts_list(search_word, response["messages"])

        if len(current_ts_list) > 0:
            current_latest_ts = min(current_ts_list)

        target_message_ts_list += current_ts_list

        if not response["has_more"]:
            print(response)
        cursor = response["response_metadata"]["next_cursor"]

    _out_to_csv(target_message_ts_list)


exec_all()
