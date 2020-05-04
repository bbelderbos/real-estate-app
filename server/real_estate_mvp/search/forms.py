from django import forms

CITY_CHOICES = [('WAW', 'Warszawa')]

PRICE_CHOICES = [(x, '{:20,.2f}'.format(x)) for x in range(0, 15000, 500)]

PROP_CHOICES = [(1, 'Mieszkanie'),
                (2, 'Pokoj'),
                (3, 'Dom')]


class SearchForm(forms.Form):
    query = forms.CharField(required=False,
                            label='Szukaj Frazy:')
    city = forms.ChoiceField(choices=CITY_CHOICES,
                             label='Miasto')
    min_rooms = forms.IntegerField(label='Min. Pokoje',
                                   min_value=0,
                                   max_value=10,
                                   required=False)
    max_rooms = forms.IntegerField(label='Max. Pokoje',
                                   min_value=0,
                                   max_value=10,
                                   required=False)
    min_price = forms.ChoiceField(choices=PRICE_CHOICES)
    max_price = forms.ChoiceField(choices=PRICE_CHOICES)
    property_type = forms.ChoiceField(choices=PROP_CHOICES)

    def clean_min_rooms(self):
        rooms = self.cleaned_data['min_rooms']
        return rooms if rooms else 0

    def clean_max_rooms(self):
        rooms = self.cleaned_data['max_rooms']
        return rooms if rooms else 10

    def clean_min_price(self):
        min_price = self.cleaned_data['min_price']
        return int(float(min_price)*100) if min_price else 0

    def clean_max_price(self):
        max_price = self.cleaned_data['max_price']
        return int(float(max_price) * 100) if max_price else 100000

    def clean(self):
        super().clean()
        cd = self.cleaned_data
        if cd['max_rooms'] < cd['min_rooms']:
            raise forms.ValidationError('Max. Pokoje musi byc wieksze niz Min.')
        if cd['max_price'] < cd['min_price']:
            raise forms.ValidationError('Max. cena musi byc wieksze niz Min.')

