# forms.py
from django import forms
from upload.models import *


class UploadForm(forms.ModelForm):

	class Meta:
		
		model = Certificate
		fields = ['updated_at', 'owner', 'file', 'points']
		labels={
			'updated_at': '', 
			'owner': '', 
			'file': '', 
			'points': ''
		}