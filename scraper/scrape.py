import requests
import json


def get_listings():
    headers = {
        "authority": "www.hemnet.se",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-SE,en;q=0.9,sv-SE;q=0.8,sv;q=0.7,fr-FR;q=0.6,fr;q=0.5,en-GB;q=0.4,en-US;q=0.3",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    }

    s = requests.Session()
    res = s.get(url="https://hemnet.se", headers=headers)
    cookies = dict(res.cookies)

    response = requests.get(
        url="https://www.hemnet.se/salda/bostader", headers=headers, cookies=cookies
    )

    html = response.text

    print(html)

    json_raw = html.split('<script type="application/ld+json">')[1].split("</script>")[
        0
    ]

    return json.loads(json_raw)


print(get_listings())
