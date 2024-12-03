import json

import requests


def main():
    print("start")
    with open('./api/payloads/payload_001.json') as f:
        payload = json.dumps(json.load(f))
        print(payload)

    url = "https://localhost:5000/v1/exports/6308d111a49a5e39f41113a0/7f935f25962e494aa1d8fc76d2f5fdfb/data"
    r = requests.post(url, data=payload, headers={"Content-Type": "application/json"})
    print(f"status code '{r.status_code}', reason '{r.reason}', content '{r.content}'")
    print("end")


if __name__ == "__main__":
    main()