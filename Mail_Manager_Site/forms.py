from django import forms
 
class PostForm(forms.Form):
    content = forms.CharField(max_length=256,widget=forms.TextInput(attrs={'class': 'form-control'}))
    created_at = forms.DateTimeField()

class SearchForm(forms.Form):
    Owner_Label_Name = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Mail_Address = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Mail_City = forms.CharField(required=False, max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Mail_State = forms.CharField(required=False, max_length=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Mail_Zip = forms.CharField(required=False, max_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Property_Address = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Property_City = forms.CharField(required=False, max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Property_State = forms.CharField(required=False, max_length=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Property_Zip = forms.IntegerField(required=False,)
    Property_Type = forms.CharField(required=False, max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Equity = forms.CharField(required=False, max_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Absentee_Owned = forms.CharField(required=False, max_length=5, widget=forms.Select(attrs={'class': 'form-control'},choices=(('empty', ''),('yes', 'Yes'),('no', 'No'),)))
    Last_Mail_Date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))