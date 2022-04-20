import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
import pandas as pd
import pytz


def round_trip(x, y):
    tree = ET.parse("xmlfiles/test_payload1.xml")
    root = tree.getroot()

    depart = root[0][2][0].text
    return_text = root[0][2][1].text

    depart_date = datetime(year=int(depart[0:4]), month=int(depart[4:6]), day=int(depart[6:8]))
    new_depart_date = depart_date + timedelta(days=x)

    return_date = datetime(year=int(return_text[0:4]), month=int(return_text[4:6]), day=int(return_text[6:8]))
    new_return_date = return_date + timedelta(days=y)

    root[0][2][0].text = new_depart_date.strftime("%Y%m%d")
    root[0][2][1].text = new_return_date.strftime("%Y%m%d")

    tree.write("output.xml")


def remove_json_element(element):
    json_payload = json.load(open("jsonfiles/test_payload.json"))
    for key in json_payload:
        value = json_payload[key]
        if key == element:
            json_payload.pop(element)
            break
        elif type(value) != str and value is not None:
            for k in value:
                if k == element:
                    json_payload[key].pop(element)
                    break

    open("jsonfiles/updated-file.json", "w").write(
        json.dumps(json_payload, sort_keys=True, indent=4, separators=(',', ': '))
    )


def read_logs(file_path):
    data = pd.read_csv(file_path)
    error_data = data[data.responseCode != 200].index
    for i in error_data:
        d = pd.to_datetime(int(data.timeStamp[i]), utc=True, unit='ms')
        pacific = pytz.timezone('US/Pacific')
        d = d.tz_convert(pacific)
        print(data.label[i], data.responseCode[i], data.responseMessage[i], data.failureMessage[i], d)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    round_trip(2, 5)
    remove_json_element("outParams")
    remove_json_element("appdate")
    read_logs("jmeterlogs/Jmeter_log1.jtl")
    read_logs("jmeterlogs/Jmeter_log2.jtl")
