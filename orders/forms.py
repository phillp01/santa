from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = [
				'first_name','last_name','email',
				'child_first_name','child_last_name', 'child_boy_girl',
				'child_age','child_age_time','child_birth_year','child_birth_month','child_birth_day',
				'child_address','child_address2','child_address3',
				'child_postal_code','child_city','child_country',
				'child_relative_name','child_friend_name',
				'child_achievement','child_present',
				'letter_design',
				'delivery_date','pdf_download','agree_terms',
		]
		widgets = {
					'letter_design' : forms.RadioSelect(),
					#'last_name' : forms.TextInput(attrs={"class": 'txt'}),
					#'email' : forms.TextInput(attrs={"class": 'txt'}),
					#'child_first_name' : forms.TextInput(attrs={"class": 'txt'}),
					#'child_last_name' : forms.TextInput(attrs={"class": 'txt'}),
					
					#'child_boy_girl' : forms.TextInput(attrs={"class": 'txt',"type": 'select'}),

		}

	def __init__(self, *args, **kwargs):
		super(OrderCreateForm, self).__init__(*args, **kwargs)

		
		
		for fname, f in self.fields.items():
			f.widget.attrs['class'] = 'txt'

		self.fields['child_age'].widget.attrs['class'] = 'txt size_sml'
		self.fields['child_age_time'].widget.attrs['class'] = 'txt size_sml last'
		self.fields['child_birth_month'].widget.attrs['class'] = 'txt size_sml2'
		self.fields['child_birth_day'].widget.attrs['class'] = 'txt size_sml2 last'
		self.fields['pdf_download'].widget.attrs['class'] = 'checkbox-custom'
		self.fields['pdf_download'].widget.attrs['id'] = 'checkbox-2'
		self.fields['agree_terms'].widget.attrs['class'] = 'checkbox-custom'
		self.fields['agree_terms'].widget.attrs['id'] = 'checkbox-3'