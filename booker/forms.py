from django import forms

class TimeForm(forms.Form):
	date_choices = (
		('empty', ''),
		('today', 'Today'),
		('tomorrow', 'Tomorrow'),
		('two', 'In two days')
	)
	date = forms.ChoiceField(
		label = "Date",
		choices = date_choices
	)

	duration_choices = (
		('empty', ''),
		('thirty', 'Half an hour'),
		('one', 'An hour'),
		('two', 'Two hours'),
		('long', 'As long as possible')
	)
	duration = forms.ChoiceField(
		label = "Duration",
		choices = duration_choices
	)

	time_choices = (
		('empty', ''),
		('now', 'Now'),
		('thirty', 'In 30 minutes'),
		('one', 'In an hour'),
		('two', 'In two hours')
	)
	time = forms.ChoiceField(
		label = "What Time?",
		choices = time_choices
	)

class AmentiesForm(forms.Form):	
	projector_option = forms.BooleanField(
		required = False,
		initial = False,
		label = "Projector"
	)
	whiteboard_option = forms.BooleanField(
		required = False,
		initial = False,
		label = "Whiteboard"
	)
	chairs_option = forms.BooleanField(
		required = False,
		initial = False,
		label = "Wheeled chairs"
	)

class LocationForm(forms.Form):	
	area_choices = (
		('empty', ''),
		('huang', 'Huang'),
		('quad', 'Main Quad'),
		('union', 'Old Union'),
		('any', 'Anywhere'),
		('other', 'Other')
	)
	area = forms.ChoiceField(
		label = "Where?",
		choices = area_choices
	)

	flexible = forms.BooleanField(
		required = False,
		initial = False,
		label = "Accept other locations?"
	)