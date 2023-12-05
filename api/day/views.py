import base64

from django.http import HttpResponse, FileResponse
from django.views.decorators.cache import cache_page

from .models import Day


def get_day(day=None):
    if day:
        return Day.objects.filter(day=day).first()

    return Day.objects.filter(day__isnull=False).order_by('-id').first()

@cache_page(60 * 10)
def day(request, day=None):
    dayObj = get_day(day)

    if not dayObj:
        return HttpResponse((
            'What are you doing? Trying to look into the future as if you are '
            'an oracle for those under your control. </br>The medium of this '
            'day is still unknown and you trying to peer again will not '
            'hasten its arrival. </br>You will have to wait like the rest '
            'of us. </br></br>I still love you though.</br></br>'
            '- <a target="_blank" href="https://chance.utc24.io">CHANCE</a>'
        ))

    image_data = base64.b64decode(dayObj.image_data)

    return HttpResponse(image_data, content_type='image/png')
