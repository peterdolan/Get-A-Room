from django import forms

class TimeForm(forms.Form):
	date_choices = (
		('empty', ''),
		('today', 'Today'),
		('tomorrow', 'Tomorrow'),
		('two', 'In two days'),
		('never', 'Never')
	)
	date = forms.ChoiceField(
		label = "Date",
		choices = date_choices
	)
