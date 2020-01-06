import csv
import slack

token = "{token}"
latest_ts = 1578296339
oldest_time = 1561906800
channel_id = "{channel_id}"
search_word = "{search_keyword}"


def _get_filtered_ts_list(search_word, message_list):
    ts_list = []
    for item in message_list:
        if item["text"] != "":
            break

        if item["subtype"] != "bot_message":
            break

        if search_word in item["attachments"][0]["fallback"]:
            break

        ts_list.append(int(float(item["ts"])))
        print(int(float(item["ts"])))

    return ts_list


def _out_to_csv(list):
    with open("./output.csv", "x") as f:
        writer = csv.writer(f)
        for item in list:
            writer.writerow([item])


def exec_all():
    client = slack.WebClient(token=token)

    cursor = None
    target_message_ts_list = []

    current_latest_ts = latest_ts

    while current_latest_ts > oldest_time:
        response = None
        if cursor is None:
            response = client.conversations_history(
                channel=channel_id, inclusive=1, oldest=oldest_time
            )
        else:
            response = client.conversations_history(
                channel=channel_id, inclusive=1, oldest=oldest_time, cursor=cursor
            )

        # retrieve last
        for item in response["messages"]:
            current_latest_ts = int(float(item["ts"]))

        target_message_ts_list.append(
            _get_filtered_ts_list(search_word, response["messages"])
        )

        if not response["has_more"]:
            break
        cursor = response["response_metadata"]["next_cursor"]

    _out_to_csv(target_message_ts_list)


exec_all()
