import base64

from django.core.exceptions import BadRequest
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

from .models import Day


def get_day(day=None):
    if day:
        return Day.objects.filter(day=day).first()

    return Day.objects.filter(day__isnull=False).order_by('-id').first()


@cache_page(60 * 60 * 24)
def day(request, day=None):
    dayObj = get_day(day)

    if not dayObj:
        raise BadRequest("Day not found")
        
    image_data = base64.b64decode(dayObj.image_data)

    return HttpResponse(image_data, content_type='image/png')
