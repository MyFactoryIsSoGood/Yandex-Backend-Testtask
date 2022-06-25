import uuid
from .models import ShopUnit
from dateutil import parser

CONTENT_404 = {"message": "Item not found"}
CONTENT_400 = {"message": "Validation Failed"}


# вспомогательная для update_categories
def update(ctg):
    children = ShopUnit.objects.filter(parentId__id=ctg.id)
    full_children = []
    if children:
        for i in children:
            if i.type == 'OFFER':
                full_children.append(i)
            else:
                full_children += update(i)
        return full_children
    else:
        return []


# обновление цен
def update_categories(categories, date):
    for category in categories:
        obj = ShopUnit.objects.get(pk=category)
        if date:
            obj.date = date
        children = update(obj)
        sum_children = sum([i.price for i in children])
        price = int(sum_children / len(children)) if children else None
        obj.price = price
        obj.save()


#проверка запроса в imports
def valid_query(query):
    if not isinstance(query, dict):
        return False
    if 'updateDate' not in query:
        return False
    if not is_date(query['updateDate']):
        return False
    if 'items' not in query:
        return False
    if not query['items']:
        return False

    ids = []
    for i in query['items']:
        if 'id' in i:
            if i['id'] in ids:
                return False
            ids.append(i['id'])
    return True


#проверка объекта для imports
def valid_item(item, units_to_post):
    if ('type' not in item) or (item['type'] not in ['OFFER', 'CATEGORY']):
        print(1)
        return False

    if ('id' not in item) or (not is_uuid(item['id'])):
        print(2)
        return False

    if ('name' not in item) or (item['name'] is None) or (item['name'] == '') or not isinstance(item['name'], str):
        print(3)
        return False

    if 'parentId' in item:
        if not ((item['parentId'] is None) or (is_uuid(item['parentId']))):
            print(4)
            return False

    if 'price' in item:
        if not isinstance(item['price'], int) or item['price'] < 0:
            print(5)
            return False
        if item['type'] == 'CATEGORY':
            if item['price'] is not None:
                print(6)
                return False

    if 'parentId' in item and item['parentId'] is not None and is_uuid(item['parentId']):
        parent_type = None
        try:
            parent_type = ShopUnit.objects.get(pk=str(item['parentId'])).type
        except ShopUnit.DoesNotExist:
            for i in units_to_post:
                if i.id == item['parentId']:
                    parent_type = i.type
                    break
        if parent_type is None or parent_type == 'OFFER':
            print(7)
            return False
    return True


def is_uuid(string):
    if string is None:
        return False
    try:
        uuid.UUID(string)
        return True
    except ValueError:
        return False


def is_date(date_str):
    try:
        date_str = parser.parse(date_str).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        print(date_str)
    except parser._parser.ParserError:
        return False
    try:
        last = date_str[-8:]
        if last == '.000000Z':
            return True
    except ValueError:
        return False
