import requests
import json

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
        "operationName": "searchForSaleListings",
        "variables": {"limit": 0, "search": {"locationIds": [473360]}},
        "query": "query location($limit: String, $location: Int)",
    }
)

response = requests.post(url, headers=headers, data=payload)

print(response.text)
