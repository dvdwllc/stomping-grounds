import settings

from scripts import loc_rec as loc_rec_util

from django.template.response import TemplateResponse

from loc_rec.locations.forms import LocationRecommendationForm
from loc_rec.locations import utils

def index(request):
    context = {'google_temp_api_key': settings.GOOGLE_MAPS_API_KEY}

    if request.method == 'POST':
        form = LocationRecommendationForm(request.POST)

        if form.is_valid():
            # sample_box =[(-100.0, 100.0), (-100.0, 100.0)]
            # items = [utils.ARRESTS, utils.GROCERY_STORES, utils.VACANCIES]
            # instances = utils.find_instances_in_bounding_box(sample_box, items)
            # print instances

            query = form.build_query()
            recommendation = loc_rec_util.recommender(query)
            recommendation.compute_maps()
            context.update({'form': form, 'best_address': recommendation.recommend_location()})

            return TemplateResponse(
                request,
                'base/recommendation_locrec.html',
                context
            )
    else:
        form = LocationRecommendationForm()

    context.update({'form': form})

    return TemplateResponse(
        request,
        'base/index.html',
        context
    )