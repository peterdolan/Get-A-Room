from django import forms

class RoomForm(forms.Form):
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

	time_choices = (
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

	capacity = forms.IntegerField(
		label = "Group Size",
		min_value = 1,
		max_value = 20,
		initial = 3
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