from flask import Flask, jsonify
import requests
from jdatetime import datetime, date

app = Flask(__name__)

api_url = "https://search.codal.ir/api/search/v2/q"


def convert_to_gregorian(persian_date):
    persian_date = datetime.strptime(persian_date, '%Y/%m/%d %H:%M:%S')
    gregorian_date = persian_date.togregorian()
    return gregorian_date.strftime("%Y-%m-%d %H:%M:%S")


def get_data_from_api():
    try:
        # Prevent being freezed by removing user-agent header
        headers = {'User-Agent': ''}
        response = requests.get(api_url, timeout=10, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX or 5XX status codes
        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None


def extract_info(data):
    info = []

    for d in data:
        info.append({
            "CompanyName": d['CompanyName'],
            "Symbol": d['Symbol'],
            "PublishDateTime": d['PublishDateTime'],
            "PublishDateTimeGregorian": convert_to_gregorian(d['PublishDateTime'])
        })

    return info


@app.route('/')
def get_publish_dates():
    data = get_data_from_api()
    info = extract_info(data['Letters'][0:3])

    if info:
        return jsonify({"error": False, "info": info})
    else:
        return jsonify({"error": True, "msg": "Failed to fetch data"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
