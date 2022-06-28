from .models import ShopUnit


# подготовка json-представления объекта
def unit_serializer(unit: ShopUnit, sales=False):
    children = ShopUnit.objects.filter(parentId__id=unit.id)
    children = list(map(unit_serializer, children))

    response = {'id': unit.id,
                'name': unit.name,
                'type': unit.type,
                'parentId': unit.parentId_id,
                'date': unit.date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z',
                'price': unit.price
                }
    if not sales:
        if unit.type == 'CATEGORY':
            response['children'] = children
        else:
            response['children'] = None
    return response
