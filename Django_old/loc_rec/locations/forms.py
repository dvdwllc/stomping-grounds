import geocoder

from django import forms


class LocationRecommendationForm(forms.Form):
    arrests = forms.BooleanField(initial=False, required=False)
    vacancies = forms.BooleanField(initial=False, required=False)
    grocery_stores = forms.BooleanField(initial=False, required=False)
    top_50 = forms.BooleanField(initial=False, required=False)
    address = forms.CharField(max_length=1000, required=False)

    def clean_address(self):
        address = self.cleaned_data['address']

        if address:
            try:
                geocoder.arcgis(address).latlng
            except:
                raise forms.ValidationError('Invalid address!')
        
        return address

    def build_query(self):
        data = self.cleaned_data
        query = []

        if data.get('address'):
            query.append(data['address'])
        else:
            query.append('22 N Green St., Baltimore, MD')

        if data.get('arrests'):
            query.append(('arrests', 'Offense', 'Unknown Offense'))
        if data.get('groceries'):
            query.append(('groceries', 'type', 'Full Supermarket'))
        if data.get('vacancies'):
            query.append('vacancies')
        if data.get('top_50'):
            query.append('top50')

        return query
