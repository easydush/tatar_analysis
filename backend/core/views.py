from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from analysis.combined import combined
from analysis.recents import recents
from analysis.shingles import shingles, unique_shingles
from comparator import canonize


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def check_view(request):
    results = {}
    file = request.FILES.get('file', None)
    if file:
        text1 = file.read().decode("utf-8")
        print(text1)
    else:
        text1 = ''.join(request.data.keys())

    with open('resources/full_merged.txt', 'r', encoding="utf-8") as file2:
        text2 = file2.read()

    text1 = canonize(text1)
    text2 = canonize(text2)

    results['Обработанный текст:'] = ' '.join(text1)
    if not len(text1):
        return Response(status=HTTP_400_BAD_REQUEST, data='Text is too short')

    results['Метод шинглов:'] = round(shingles(text1, text2), 2)
    results['Метод уникальных шинглов:'] = round(unique_shingles(text1, text2), 2)
    results['Метод наиболее встречающихся:'] = round(recents(text1, text2), 2)
    results['Комбинация методов:'] = round(combined(text1, text2), 2)

    return Response(results)
