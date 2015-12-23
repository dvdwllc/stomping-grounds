from scripts import loc_rec as loc_rec_util

from django.template.response import TemplateResponse

from loc_rec.locations.forms import LocationRecommendationForm

def index(request):
    context = {}

    if request.method == 'POST':
        form = LocationRecommendationForm(request.POST)

        if form.is_valid():
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