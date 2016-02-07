from django import forms

class TimeForm(forms.Form):
	date_choices = (
		('today', 'Today'),
		('tomorrow', 'Tomorrow'),
		('two', 'In two days')
	)
	date = forms.ChoiceField(
		label = "Date",
		required = False,
		choices = date_choices,
		initial = 'today'
	)

	duration_choices = (
		('thirty', 'Half an hour'),
		('one', 'An hour'),
		('two', 'Two hours'),
		('long', 'As long as possible')
	)
	duration = forms.ChoiceField(
		label = "Duration",
		required = False,
		choices = duration_choices,
		initial = 'one'
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
		required = False,
		choices = time_choices,
		initial = 'now'
	)

	projector = forms.BooleanField(
		required = False,
		initial = False,
		label = "Projector"
	)
	whiteboard = forms.BooleanField(
		required = False,
		initial = False,
		label = "Whiteboard"
	)
	windows = forms.BooleanField(
		required = False,
		initial = False,
		label = "Windows"
	)

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
		required = False,
		choices = area_choices
	)

	flexible = forms.BooleanField(
		required = False,
		initial = False,
		label = "Accept other locations?"
	)