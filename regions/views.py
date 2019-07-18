# django
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

# models
from regions.models import Commune


@login_required
def search_communes(request):
    """ View that searches an office """

    commune = request.GET.get('commune')
    region_id = request.GET.get('regionId')

    if commune:
        communes = Commune.objects.filter(
            Q(id__startswith=commune) |
            Q(name__icontains=commune)
        )
    else:
        communes = Commune.objects.all()

    if region_id and int(region_id):
        communes = communes.filter(region_id=region_id)

    communes = communes.order_by('id')

    results = []
    for commune in communes:
        commune_dict = {
            'id': commune.id,
            'text': u'{} - {}'.format(commune.id, commune.name)
        }
        results.append(commune_dict)

    return JsonResponse(results, safe=False)
