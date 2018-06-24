from django import forms
from datetime import timedelta


class SplitDurationWidget(forms.MultiWidget):
    """
    A Widget that splits duration input into four number input boxes.
    """

    def __init__(self, attrs=None):
        widgets = (forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs),
                   forms.NumberInput(attrs=attrs))
        super(SplitDurationWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            d = value
            if d:
                weeks = d.days // 7
                days = (d.days % 7) % 7
                hours = d.seconds // 3600
                minutes = (d.seconds % 3600) // 60
                seconds = d.seconds % 60
                return [weeks, days, hours, minutes]
        return [0, 0, 0, 0]


class MultiValueDurationField(forms.MultiValueField):
    widget = SplitDurationWidget(
        attrs={
            'class': 'interval-input',
            'min': 0
        }
    )

    def __init__(self, label, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
            forms.IntegerField(),
            forms.IntegerField(),
        )
        super(MultiValueDurationField, self).__init__(
            label=label,
            fields=fields,
            require_all_fields=True, *args, **kwargs)

    def compress(self, data_list):
        if len(data_list) == 4:
            return timedelta(
                weeks=int(data_list[0]),
                days=int(data_list[1]),
                hours=int(data_list[2]),
                minutes=int(data_list[3]))
        else:
            return timedelta(0)