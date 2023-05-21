import requests
import json


def load_menu():
    s = requests.Session()

    htmlHeaders = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    }

    r = s.get(
        "https://www.myschoolmenus.com/organizations/1184/sites/9282/menus/36757",
        headers=htmlHeaders,
    )

    cookies_dict = r.cookies.get_dict()
    XSRF_TOKEN = cookies_dict["XSRF-TOKEN"]

    jsonHeaders = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-district": "1184",
        "x-requested-with": "XMLHttpRequest",
        "x-xsrf-token": XSRF_TOKEN,
    }

    response = s.get(
        "https://www.myschoolmenus.com/api/public/menus/36757",
        headers=jsonHeaders,
    )

    json_dict = json.loads(response.text)
    menu_month_calendar = json_dict["data"]["menu_month_calendar"]
    res_obj = {"title": json_dict["data"]["menu_info"]["menu_title"], "menu_days": []}

    for menu in menu_month_calendar:
        date = menu["day"]
        setting = json.loads(menu["setting"])
        items = setting["current_display"]
        category = ""
        my_items = []
        for item in items:
            if item["type"] == "category":
                category_name = item["name"]
                if category_name != category:
                    category = category_name
            elif item["type"] == "recipe":
                my_items.append(
                    {
                        "category": category,
                        "name": item["name"],
                        "weight": item["weight"],
                    }
                )
        day_menu = {"date": date, "items": my_items}
        res_obj["menu_days"].append(day_menu)

    return res_obj
