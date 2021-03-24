#!/usr/bin/env python3

import requests
import json

catalog = {
    6: 'ipc',
    5: 'dvr',
}

#curl 'https://baike.xm030.cn/download/pagination.do' --data-raw 'page=1&rows=50&paramValue=5'
def get_rows(param, num):
    update_url = f"https://baike.xm030.cn/download/pagination.do?page=1&rows={num}&paramValue={param}"
    r = requests.get(update_url)
    return r.json()


def main():

    for i in catalog:
        total = get_rows(i, 1)['total']
        items = get_rows(i, total)
        fname = f"items.{catalog[i]}"
        print(f"Writing {fname}...")
        with open(fname, "w") as f:

            f.write(json.dumps(items, sort_keys=True, indent=4))


if __name__ == '__main__':
    main()
