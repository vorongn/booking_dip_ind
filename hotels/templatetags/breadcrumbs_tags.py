from django import template
from django.urls import reverse
import hotels.views as views
from hotels.models import Hotel, Room

register = template.Library()


@register.simple_tag
def breadcrumbs(request):
    breadcrumbs = []
    path_components = request.path.split("/")
    url_so_far = ""
    for component in path_components:
        if component:
            url_so_far += f"/{component}"
            try:
                # Используйте reverse с использованием slug вместо имени представления
                view_name = reverse(url_so_far[1:])
                breadcrumbs.append((view_name, component))
            except:
                pass
    return breadcrumbs
