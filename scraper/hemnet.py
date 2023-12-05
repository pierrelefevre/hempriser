import requests
import json


def get_urls(location_id, page):
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

    try:
        response = requests.get(
            url=f"https://www.hemnet.se/salda/bostader?location_ids%5B%5D={location_id}&page={page}",
            headers=headers,
            cookies=cookies,
        )

        html = response.text

        json_raw = html.split('<script type="application/ld+json">')[1].split(
            "</script>"
        )[0]

        parsed = json.loads(json_raw)

        urls = []

        for listing in parsed["itemListElement"]:
            urls.append(listing["url"])

        return urls

    except:
        return []


def get_single_listing(url: str):
    headers = {
        "authority": "www.hemnet.se",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-SE,en;q=0.9,sv-SE;q=0.8,sv;q=0.7,fr-FR;q=0.6,fr;q=0.5,en-GB;q=0.4,en-US;q=0.3",
        "cache-control": "no-cache",
        "cookie": "_hemnet_listing_result_settings_sorting=creation+desc; _hemnet_listing_result_settings_list=normal; hn_usr_bkt=%7B%22resultPages%22%3A52%2C%22listingPagesV2%22%3A44%7D; hn_usr_bkt_config=%7B%22listingPages%22%3A100%2C%22resultPages%22%3A100%7D; CF_AppSession=nd636d2f9f74c29f8; hn_exp_kpis=455; hn_exp_bsp=665; hn_exp_ail=454; hn_tag_bkt=436; __cfruid=f4d8d22701a4aab078ed5d4314a2ec754b361453-1701767336; AWSALB=6qsw4pwUoWoyFTqcwvsE3qXT/SUFNx+md19Gl2RFFl/SQbHpns7407QktcIqjLE4LS/qdHSX7KW/1p/HgNRSvxWWFkLv86K8XX+84eOVVGgasQX5ciH7ImKvzKTT; AWSALBCORS=6qsw4pwUoWoyFTqcwvsE3qXT/SUFNx+md19Gl2RFFl/SQbHpns7407QktcIqjLE4LS/qdHSX7KW/1p/HgNRSvxWWFkLv86K8XX+84eOVVGgasQX5ciH7ImKvzKTT; hn_uc_consent={%22Usercentrics%20Consent%20Management%20Platform%22:true%2C%22Google%20Maps%22:true%2C%22Google%20Tag%20Manager%22:true%2C%22Bambuser%22:true%2C%22Datadog%22:true%2C%22Cloudflare%22:true%2C%22Vimeo%22:true%2C%22YouTube%20Video%22:true%2C%22Klarna%22:true%2C%22Firebase%20Remote%20Config%22:true%2C%22Firebase%20Crashlytics%22:true%2C%22Firebase%20Cloud%20Messaging%20(FCM)%22:true%2C%22Matterport%22:true%2C%22Humany%22:true%2C%22Sentry%22:true%2C%22Hemnets%20egna%20n%C3%B6dv%C3%A4ndiga%20verktyg%22:true%2C%22Amazon%20Web%20Services%22:true%2C%22Google%20Ads%22:false%2C%22Google%20Analytics%22:false%2C%22Google%20Optimize%22:false%2C%22Hotjar%22:false%2C%22Firebase%20Performance%20Monitoring%22:false%2C%22The%20Kantar%20Group%22:false}; _dd_s=rum=0&expire=1701768316395",
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
    try:
        s = requests.Session()
        res = s.get(url="https://hemnet.se", headers=headers)
        cookies = dict(res.cookies)

        response = requests.get(url, headers=headers, cookies=cookies)

        html = response.text

        json_raw = html.split('<script id="__NEXT_DATA__" type="application/json">')[
            1
        ].split("</script>")[0]

        json_data = json.loads(json_raw)
        return json_data

    except Exception:
        return None


def get_location_ids(query: str = "gamla stan", limit: int = 2000):
    url = "https://www.hemnet.se/graphql"

    headers = {
        "authority": "www.hemnet.se",
        "accept": "*/*",
        "accept-language": "en-SE,en;q=0.9,sv-SE;q=0.8,sv;q=0.7,fr-FR;q=0.6,fr;q=0.5,en-GB;q=0.4,en-US;q=0.3",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "cookie": "hn_usr_bkt_config=%7B%22listingPages%22%3A100%2C%22resultPages%22%3A100%7D; hn_usr_bkt=%7B%22resultPages%22%3A32%2C%22listingPagesV2%22%3A88%7D; hn_tag_bkt=362; __cfruid=4abc99352676204790b63edaae3d9ba8f42bfb70-1701768112; hn_uc_consent={%22Google%20Ads%22:false%2C%22Usercentrics%20Consent%20Management%20Platform%22:true%2C%22Google%20Maps%22:true%2C%22Google%20Tag%20Manager%22:true%2C%22Bambuser%22:true%2C%22Datadog%22:true%2C%22Cloudflare%22:true%2C%22Vimeo%22:true%2C%22YouTube%20Video%22:true%2C%22Klarna%22:true%2C%22Firebase%20Remote%20Config%22:true%2C%22Firebase%20Crashlytics%22:true%2C%22Firebase%20Cloud%20Messaging%20(FCM)%22:true%2C%22Matterport%22:true%2C%22Humany%22:true%2C%22Sentry%22:true%2C%22Hemnets%20egna%20n%C3%B6dv%C3%A4ndiga%20verktyg%22:true%2C%22Amazon%20Web%20Services%22:true%2C%22Google%20Analytics%22:false%2C%22Google%20Optimize%22:false%2C%22Hotjar%22:false%2C%22Firebase%20Performance%20Monitoring%22:false%2C%22The%20Kantar%20Group%22:false}; CF_AppSession=na8e1b06197099960; AWSALB=3ShUqe9vfsv8aYHEAZuyta3jgX36pB6DgmY8F889XAsYG1FLY1jy8iydpm1H3t9FE3b8RCourMizB0Pf2shz3UJ+1Phg711DYr28ytvYBWFsUENRgbZyTM5fW6hh; AWSALBCORS=3ShUqe9vfsv8aYHEAZuyta3jgX36pB6DgmY8F889XAsYG1FLY1jy8iydpm1H3t9FE3b8RCourMizB0Pf2shz3UJ+1Phg711DYr28ytvYBWFsUENRgbZyTM5fW6hh; _dd_s=rum=0&expire=1701770935838",
        "dnt": "1",
        "hemnet-application-version": "www-0.0.1",
        "origin": "https://www.hemnet.se",
        "pragma": "no-cache",
        "referer": "https://www.hemnet.se/bostader",
        "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }

    payload = json.dumps(
        {
            "operationName": "locationSearch",
            "variables": {"searchString": query, "limit": limit},
            "query": "query locationSearch($searchString: String\u0021, $limit: Int\u0021) {\n  autocompleteLocations(\nquery: $searchString\nlimit: $limit\n){\nhits{\nlocation{\nid\nfullName\nparentFullName\ntype\n}}}}",
        }
    )
    response = requests.post(url, headers=headers, data=payload)

    try:
        json_data = response.json()
        hits = json_data["data"]["autocompleteLocations"]["hits"]

        locs = []

        for location in hits:
            loc = {}

            loc["id"] = location["location"]["id"]
            loc["fullName"] = location["location"]["fullName"]
            loc["parentFullName"] = location["location"]["parentFullName"]
            loc["type"] = location["location"]["type"]

            locs.append(loc)

    except:
        print("Error getting location ids")

    return locs


if __name__ == "__main__":
    urls = get_urls(location_id="473360", page=1)
    print(json.dumps(urls))
