from .utils import is_uuid, is_date, valid_item, valid_query, update_categories, CONTENT_404, CONTENT_400

from datetime import timedelta
from dateutil import parser
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import ShopUnit
from .serializers import unit_serializer


@api_view(['POST'])
def imports(request):
    categories_to_update = []
    units_to_post = []
    if request.method == 'POST':
        if valid_query(request.data):
            date = request.data['updateDate']
            date = parser.parse(date).strftime("%Y-%m-%dT%H:%M:%S.%S0Z")
            for unit in request.data['items']:  # Проверяем и формируем список объектов на публикацию
                if valid_item(unit, units_to_post):
                    try:
                        ShopUnit.objects.get(pk=unit['id'])
                        obj = ShopUnit.objects.get(pk=unit['id'])
                        if obj.type != unit['type']:
                            return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)
                    except ShopUnit.DoesNotExist:
                        obj = ShopUnit()
                    obj.id = unit['id']
                    obj.name = unit['name']
                    obj.parentId_id = unit['parentId'] if 'parentId' in unit else None
                    obj.type = unit['type']
                    obj.date = date
                    if obj.type == 'OFFER':
                        obj.price = unit['price'] if 'price' in unit else 0
                    else:
                        obj.price = None
                    if obj.type == 'CATEGORY':
                        categories_to_update.append(obj.id)
                    units_to_post.append(obj)
                else:
                    return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)

            for unit in units_to_post:  # Формируем список категорий к обновлению цены и публикуем
                category = unit.parentId_id
                if category and category not in categories_to_update:
                    categories_to_update.append(category)
                    climbing = True
                    possible = category
                    while climbing:  # Добавляем все супер категории в список для обновления
                        possible = ShopUnit.objects.get(pk=possible)
                        if possible.parentId_id:
                            if possible.parentId_id not in categories_to_update:
                                categories_to_update.append(str(possible.parentId_id))
                                possible = possible.parentId_id
                        else:
                            climbing = False
                unit.save()
            if categories_to_update:
                update_categories(categories_to_update, date)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete(request, unit_id):
    if request.method == 'DELETE':
        categories_to_update = []
        if not is_uuid(unit_id):
            return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)
        try:
            unit = ShopUnit.objects.get(pk=unit_id)
            category = unit.parentId_id
            if category and category not in categories_to_update:
                categories_to_update.append(category)
                climbing = True
                possible = category
                while climbing:  # Добавляем все супер категории в список для обновления
                    possible = ShopUnit.objects.get(pk=possible)
                    if possible.parentId_id:
                        if possible.parentId_id not in categories_to_update:
                            categories_to_update.append(possible.parentId_id)
                            possible = possible.parentId_id
                    else:
                        climbing = False
            if categories_to_update:
                update_categories(categories_to_update, date=None)
            unit.delete()
            return Response(status=status.HTTP_200_OK)
        except ShopUnit.DoesNotExist:
            return Response(CONTENT_404, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def nodes(request, unit_id):
    if request.method == 'GET':
        if not is_uuid(unit_id):
            return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)

        try:
            unit = ShopUnit.objects.get(pk=unit_id)
            response = unit_serializer(unit)
            return JsonResponse(response)

        except ShopUnit.DoesNotExist:
            return Response(CONTENT_404, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def sales(request):
    if request.method == 'GET':
        items = []
        if 'date' in request.query_params:
            if len(request.query_params) > 1:
                return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)
            date = request.query_params['date']
            if is_date(date):
                date = parser.parse(date).strftime("%Y-%m-%dT%H:%M:%S.%S0Z")
                date = parser.parse(date)

                start_time = date - timedelta(days=1)
                units = ShopUnit.objects.filter(date__range=[start_time, date], type='OFFER')
                for i in units:
                    items.append(unit_serializer(i, sales=True))

                content = {
                    'items': items
                }
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def node_stats(request, unit_id):
    if request.method == 'GET':
        dates = []
        items = []

        if not is_uuid(unit_id):
            return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)

        if 'dateStart' not in request.query_params or 'dateEnd' not in request.query_params or not is_date(
                request.query_params['dateStart'] or not is_date(request.query_params['dateEnd'])):
            return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)

        if len(request.query_params) > 2:
            return Response(CONTENT_400, status=status.HTTP_400_BAD_REQUEST)

        start = request.query_params['dateStart']
        start = parser.parse(start).strftime("%Y-%m-%dT%H:%M:%S.%S0Z")
        start = parser.parse(start)

        end = request.query_params['dateEnd']
        end = parser.parse(end).strftime("%Y-%m-%dT%H:%M:%S.%S0Z")
        end = parser.parse(end)

        try:
            unit = ShopUnit.objects.get(pk=unit_id)
            stats = unit.stats.all()
            for i in stats:
                if i.date not in dates and start <= i.date < end:
                    items.append(unit_serializer(i, True))
                    dates.append(i.date)
            response = {'items': items}
            return Response(response, status=status.HTTP_200_OK)

        except ShopUnit.DoesNotExist:
            return Response(CONTENT_404, status=status.HTTP_404_NOT_FOUND)
