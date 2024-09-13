from .jumia import jumiaProductScraper,ProductUrlScraper
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from concurrent.futures import ThreadPoolExecutor


@api_view(['GET'])
@permission_classes([AllowAny])
def get_product(request, name):
    jumiaScraper = ProductUrlScraper(f"https://www.jumia.ma/catalog/?q={name}", 'https://www.jumia.ma', 5)
    jumiaScraper.get_html()
    jumiaScraper.parse_html()

    urls = jumiaScraper.get_data()
    with ThreadPoolExecutor(max_workers=5) as executor:
        res = list(executor.map(jumiaProductScraper,urls))

    return Response(res)




