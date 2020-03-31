import re
import urllib
from datetime import date, datetime
from slack import WebClient

token = ""

user_id = ""
start_dt = date(2020, 3, 1)
end_dt = date(2020, 3, 29)


def search_messages(query):
    message_list = []

    s_quote = urllib.parse.quote(query)
    client = WebClient(token=token)

    for i in range(0, 100):
        data = client.search_messages(query=s_quote, page=i, sort="timestamp", sort_dir="asc")
        print(data.data['ok'], data.data["messages"]["paging"]["pages"], data.data["messages"]["paging"]["page"])

        message_list.extend(data.data["messages"]["matches"])
        if data.data["messages"]["paging"]["pages"] == 0:
            print("could not find")
            break
        if data.data["messages"]["paging"]["pages"] == data.data["messages"]["paging"]["page"]:
            break

    return message_list


def convert_to_dict(response_dict_list):
    msg_array = []
    msg_dict = {
        'ts': [],
        'parent_ts': [],
        'is_parent': [],
        'text': [],
        'permalink': [],
    }

    for elm in response_dict_list:
        m = re.search('[0-9]*\.[0-9]*$', elm["permalink"])
        parent_ts = 0
        if m is not None:
            parent_ts = m.group(0)

        msg_dict['ts'].append(datetime.fromtimestamp(float(elm["ts"])))
        msg_dict['parent_ts'].append(datetime.fromtimestamp(float(parent_ts)))
        msg_dict['is_parent'].append(elm["ts"] == parent_ts)
        msg_dict['text'].append(elm["text"])
        msg_dict['permalink'].append(elm["permalink"])

        msg_array.append({
            'ts': datetime.fromtimestamp(float(elm["ts"])),
            'parent_ts': datetime.fromtimestamp(float(parent_ts)),
            'is_parent': elm["ts"] == parent_ts,
            'text': elm["text"],
            'permalink': elm["permalink"],
        })

    result = []
    for i in msg_array:
        if i['parent_ts'] in msg_dict['ts']:
            result.append(i)

    return result


def output(msg_array):
    start_day = 0
    for i in msg_array:
        each_start_dt = i['ts'].day
        if each_start_dt != start_day:
            print(datetime.strftime(i['ts'], "%m/%d"))
        start_day = each_start_dt
        print(" {}, {}, {}".format(
            datetime.strftime(i['ts'], "%H:%M"),
            re.sub(r'<.*\||\n|>', '', i['text']),
            i['permalink'],
        ))


query = "in:#eureka-attendance after:{} before:{} from:@{}".format(
    start_dt.strftime("%Y-%m-%d"),
    end_dt.strftime("%Y-%m-%d"),
    user_id
)
print(query)
msg_response_dict = search_messages(query)
msg_arr = convert_to_dict(msg_response_dict)
output(msg_arr)
