#!/usr/bin/env python3

import json

import requests
import urllib3

CATALOGS = {
    6: "ipc",
    5: "dvr",
}

PAGINATION_URL = "https://baike.xm030.cn/download/pagination.do"

# Vendor TLS cert is stale (issued for a different domain, expired in 2019).
# Disable verification only for this host.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_rows(param, num):
    r = requests.get(
        PAGINATION_URL,
        params={"page": 1, "rows": num, "paramValue": param},
        verify=False,
        timeout=60,
    )
    r.raise_for_status()
    return r.json()


def clean_row(row):
    url = row.get("downloadUrl")
    if isinstance(url, str):
        row["downloadUrl"] = url.strip()
    return row


def main():
    for param, suffix in CATALOGS.items():
        total = get_rows(param, 1)["total"]
        items = get_rows(param, total)
        items["rows"] = sorted((clean_row(r) for r in items["rows"]), key=lambda r: r["id"])
        fname = f"items.{suffix}"
        print(f"Writing {fname} ({len(items['rows'])} rows)...")
        with open(fname, "w") as f:
            json.dump(items, f, sort_keys=True, indent=4)
            f.write("\n")


if __name__ == "__main__":
    main()
