
import pdb

from loc_rec.locations import models as location_models


ARRESTS = 'arrests'
VACANCIES = 'vacancies'
GROCERY_STORES = 'grocery_stores'
RESTAURANTS = 'restaurants'
TOP_50 = 'top_50'

ITEM_MAPPING = {
    ARRESTS: location_models.Arrest,
    VACANCIES: location_models.Vacancy,
    GROCERY_STORES: location_models.GroceryStore,
    RESTAURANTS: location_models.Restaurant,
}

def build_coordinate_filter_kwargs(bounding_box):
    [lat_boundaries, long_boundaries] = bounding_box
    lat_min, lat_max = lat_boundaries
    long_min, long_max = long_boundaries

    return {
        'latitude__lte': lat_max,
        'latitude__gte': lat_min,
        'longitude__lte': long_max,
        'longitude__gte': long_min,
    }


def find_instances_in_bounding_box(bounding_box, items):
    """
    bounding_box :: [(lat_min, lat_max),(long_min, long_max)]
    items is the list of items you want to query on, e.g.: [ARRESTS, VACANCIES].
    """
    filter_kwargs = build_coordinate_filter_kwargs(bounding_box)
    result = {}

    for item in items:
        if not item in ITEM_MAPPING.keys() and item is not TOP_50:
            raise ValueError('{item} is not a valid item.'.format(item=item))

        model = ITEM_MAPPING[item]
        result[item] = model.objects.filter(**filter_kwargs)

    return result