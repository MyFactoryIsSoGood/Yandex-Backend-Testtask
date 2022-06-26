# encoding=utf8

import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASEURL = "http://10.22.3.234"

ROOT_ID = "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"

IMPORT_BATCHES = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Товары",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "parentId": None
            }
        ],
        "updateDate": "2022-02-01T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Смартфоны",
                "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "jPhone 13",
                "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 79999
            },
            {
                "type": "OFFER",
                "name": "Xomiа Readme 10",
                "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                "price": 59999
            }
        ],
        "updateDate": "2022-02-02T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Телевизоры",
                "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            },
            {
                "type": "OFFER",
                "name": "Samson 70\" LED UHD Smart",
                "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 32999
            },
            {
                "type": "OFFER",
                "name": "Phyllis 50\" LED UHD Smarter",
                "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 49999
            }
        ],
        "updateDate": "2022-02-03T12:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "Goldstar 65\" LED UHD LOL Very Smart",
                "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                "price": 69999
            }
        ],
        "updateDate": "2022-02-03T15:00:00.000Z"
    }
]

MY_IMPORT = [
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "first",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "parentId": None
            },
            {
                "type": "OFFER",
                "name": "1",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "price": 5
            },
            {
                "type": "OFFER",
                "name": "2",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a333",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "price": 8
            },
            {
                "type": "CATEGORY",
                "name": "second",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a444",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111"
            }
        ],
        "updateDate": "2022-01-01T00:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "first1",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "parentId": None
            }
        ],
        "updateDate": "2022-01-01T01:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "first2",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "parentId": None
            }
        ],
        "updateDate": "2022-01-01T02:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "CATEGORY",
                "name": "first3",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "parentId": None
            }
        ],
        "updateDate": "2022-01-01T03:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "1 NEW",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "price": 50
            }
        ],
        "updateDate": "2022-01-01T04:00:00.000Z"
    },
    {
        "items": [
            {
                "type": "OFFER",
                "name": "1 NEW NEW",
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
                "price": 500
            }
        ],
        "updateDate": "2022-01-01T05:00:00.000Z"
    },
]

EXPECTED_TREE = {
    "type": "CATEGORY",
    "name": "Товары",
    "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    "price": 58599,
    "parentId": None,
    "date": "2022-02-03T15:00:00.000Z",
    "children": [
        {
            "type": "CATEGORY",
            "name": "Телевизоры",
            "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 50999,
            "date": "2022-02-03T15:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "Samson 70\" LED UHD Smart",
                    "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 32999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None,
                },
                {
                    "type": "OFFER",
                    "name": "Phyllis 50\" LED UHD Smarter",
                    "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 49999,
                    "date": "2022-02-03T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Goldstar 65\" LED UHD LOL Very Smart",
                    "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
                    "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
                    "price": 69999,
                    "date": "2022-02-03T15:00:00.000Z",
                    "children": None
                }
            ]
        },
        {
            "type": "CATEGORY",
            "name": "Смартфоны",
            "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
            "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
            "price": 69999,
            "date": "2022-02-02T12:00:00.000Z",
            "children": [
                {
                    "type": "OFFER",
                    "name": "jPhone 13",
                    "id": "863e1a7a-1304-42ae-943b-179184c077e3",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 79999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                },
                {
                    "type": "OFFER",
                    "name": "Xomiа Readme 10",
                    "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
                    "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
                    "price": 59999,
                    "date": "2022-02-02T12:00:00.000Z",
                    "children": None
                }
            ]
        },
    ]
}
EXPECTED_STATS = {
    "items": [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "name": "first3",
            "type": "CATEGORY",
            "parentId": None,
            "date": "2022-01-01T05:00:00.000Z",
            "price": 254
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "name": "first3",
            "type": "CATEGORY",
            "parentId": None,
            "date": "2022-01-01T04:00:00.000Z",
            "price": 29
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "name": "first3",
            "type": "CATEGORY",
            "parentId": None,
            "date": "2022-01-01T03:00:00.000Z",
            "price": 6
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "name": "first2",
            "type": "CATEGORY",
            "parentId": None,
            "date": "2022-01-01T02:00:00.000Z",
            "price": 6
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "name": "first1",
            "type": "CATEGORY",
            "parentId": None,
            "date": "2022-01-01T01:00:00.000Z",
            "price": 6
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "name": "first",
            "type": "CATEGORY",
            "parentId": None,
            "date": "2022-01-01T00:00:00.000Z",
            "price": 6
        }
    ]
}
EXPECTED_STATS_CROP = {
    "items": [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "name": "first3",
            "type": "CATEGORY",
            "parentId": None,
            "date": "2022-01-01T04:00:00.000Z",
            "price": 29
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "name": "first3",
            "type": "CATEGORY",
            "parentId": None,
            "date": "2022-01-01T03:00:00.000Z",
            "price": 6
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "name": "first2",
            "type": "CATEGORY",
            "parentId": None,
            "date": "2022-01-01T02:00:00.000Z",
            "price": 6
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "name": "first1",
            "type": "CATEGORY",
            "parentId": None,
            "date": "2022-01-01T01:00:00.000Z",
            "price": 6
        }
    ]
}
EXPECTED_STATS_OFFER = {
    "items": [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
            "name": "1 NEW NEW",
            "type": "OFFER",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "date": "2022-01-01T05:00:00.000Z",
            "price": 500
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
            "name": "1 NEW",
            "type": "OFFER",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "date": "2022-01-01T04:00:00.000Z",
            "price": 50
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
            "name": "1",
            "type": "OFFER",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "date": "2022-01-01T00:00:00.000Z",
            "price": 5
        }
    ]
}
EXPECTED_STATS_OFFER_CROP = {
    "items": [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
            "name": "1 NEW",
            "type": "OFFER",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "date": "2022-01-01T04:00:00.000Z",
            "price": 50
        }
    ]
}
EXPECTED_SALES = {
    "items": [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a333",
            "name": "2",
            "type": "OFFER",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "date": "2022-01-01T00:00:00.000Z",
            "price": 8
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
            "name": "1 NEW NEW",
            "type": "OFFER",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "date": "2022-01-01T05:00:00.000Z",
            "price": 500
        }
    ]
}
EXPECTED_SALES_CROPPED = {
    "items": [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66a222",
            "name": "1 NEW NEW",
            "type": "OFFER",
            "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a111",
            "date": "2022-01-01T05:00:00.000Z",
            "price": 500
        }
    ]
}


def request(path, method="GET", data=None, json_response=False):
    try:
        params = {
            "url": f"{API_BASEURL}{path}",
            "method": method,
            "headers": {},
        }

        if data:
            params["data"] = json.dumps(
                data, ensure_ascii=False).encode("utf-8")
            params["headers"]["Content-Length"] = len(params["data"])
            params["headers"]["Content-Type"] = "application/json"

        req = urllib.request.Request(**params)

        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode("utf-8")
            if json_response:
                res_data = json.loads(res_data)
            return (res.getcode(), res_data)
    except urllib.error.HTTPError as e:
        return (e.getcode(), None)


def deep_sort_children(node):
    if node.get("children"):
        node["children"].sort(key=lambda x: x["id"])

        for child in node["children"]:
            deep_sort_children(child)


def print_diff(expected, response):
    with open("expected.json", "w") as f:
        json.dump(expected, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    with open("response.json", "w") as f:
        json.dump(response, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")

    subprocess.run(["git", "--no-pager", "diff", "--no-index",
                    "expected.json", "response.json"])


def test_import(my=False):
    for index, batch in enumerate(IMPORT_BATCHES if not my else MY_IMPORT):
        print(f"Importing batch {index}")
        status, _ = request("/imports", method="POST", data=batch)

        assert status == 200, f"Expected HTTP status code 200, got {status}"

    print("Test import passed.")


def test_nodes():
    status, response = request(f"/nodes/{ROOT_ID}", json_response=True)
    # print(json.dumps(response, indent=2, ensure_ascii=False))

    assert status == 200, f"Expected HTTP status code 200, got {status}"

    deep_sort_children(response)
    deep_sort_children(EXPECTED_TREE)
    if response != EXPECTED_TREE:
        print_diff(EXPECTED_TREE, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    print("Test nodes passed.")


def test_sales():
    params = urllib.parse.urlencode({
        "date": "2022-02-04T00:00:00.000Z"
    })
    status, response = request(f"/sales?{params}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    print("Test sales passed.")


def test_mysales():
    params = urllib.parse.urlencode({
        "date": "2022-01-01T05:00:00.000Z"
    })
    status, response = request(f"/sales?{params}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    if response != EXPECTED_SALES:
        print_diff(EXPECTED_SALES, response)
        print("Response tree doesn't match expected")
        sys.exit(1)
    print("Test sales passed.")

    params = urllib.parse.urlencode({
        "date": "2022-01-02T05:00:00.000Z"
    })
    status, response = request(f"/sales?{params}", json_response=True)
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    if response != EXPECTED_SALES_CROPPED:
        print_diff(EXPECTED_SALES_CROPPED, response)
        print("Response tree doesn't match expected")
        sys.exit(1)
    print("Test sales cropped passed.")


def test_mystats():
    params = urllib.parse.urlencode({
        "dateStart": "2020-02-01T00:00:00.000Z",
        "dateEnd": "2025-02-03T00:00:00.000Z"
    })
    status, response = request(
        f"/node/3fa85f64-5717-4562-b3fc-2c963f66a111/statistic?{params}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"
    if response != EXPECTED_STATS:
        print_diff(EXPECTED_STATS, response)
        print("Response tree doesn't match expected")
        sys.exit(1)

    status, response = request(
        f"/node/3fa85f64-5717-4562-b3fc-2c963f66a222/statistic?{params}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"
    if response != EXPECTED_STATS_OFFER:
        print_diff(EXPECTED_STATS_OFFER, response)
        print("Response tree doesn't match expected")
        sys.exit(1)
    print("Test stats passed.")

    params = urllib.parse.urlencode({
        "dateStart": "2022-01-01T00:00:01.000Z",
        "dateEnd": "2022-01-01T05:00:00.000Z"
    })

    status, response = request(
        f"/node/3fa85f64-5717-4562-b3fc-2c963f66a111/statistic?{params}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"
    if response != EXPECTED_STATS_CROP:
        print_diff(EXPECTED_STATS_CROP, response)
        print("Response tree doesn't match expected")
        sys.exit(1)

    status, response = request(
        f"/node/3fa85f64-5717-4562-b3fc-2c963f66a222/statistic?{params}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"
    if response != EXPECTED_STATS_OFFER_CROP:
        print_diff(EXPECTED_STATS_OFFER_CROP, response)
        print("Response tree doesn't match expected")
        sys.exit(1)
    print("Test stats cropped passed.")


def test_stats():
    params = urllib.parse.urlencode({
        "dateStart": "2020-02-01T00:00:00.000Z",
        "dateEnd": "2025-02-03T00:00:00.000Z"
    })
    status, response = request(
        f"/node/{ROOT_ID}/statistic?{params}", json_response=True)

    assert status == 200, f"Expected HTTP status code 200, got {status}"
    print("Test stats passed.")


def test_delete():
    status, _ = request(f"/delete/{ROOT_ID}", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"

    status, _ = request(f"/nodes/{ROOT_ID}", json_response=True)
    assert status == 404, f"Expected HTTP status code 404, got {status}"

    print("Test delete passed.")


def delete_my():
    status, _ = request(f"/delete/3fa85f64-5717-4562-b3fc-2c963f66a111", method="DELETE")
    assert status == 200, f"Expected HTTP status code 200, got {status}"
    print("Test delete passed.")


def test_all():
    test_import()
    # test_nodes()
    # test_sales()
    # test_stats()
    # test_delete()
    # print('____________')
    # print('Your tests:')
    test_import(my=True)
    # test_mysales()
    # test_mystats()
    # delete_my()


def main():
    global API_BASEURL
    test_name = None

    for arg in sys.argv[1:]:
        if re.match(r"^https?://", arg):
            API_BASEURL = arg
        elif test_name is None:
            test_name = arg

    if API_BASEURL.endswith('/'):
        API_BASEURL = API_BASEURL[:-1]

    if test_name is None:
        test_all()
    else:
        test_func = globals().get(f"test_{test_name}")
        if not test_func:
            print(f"Unknown test: {test_name}")
            sys.exit(1)
        test_func()


if __name__ == "__main__":
    main()
