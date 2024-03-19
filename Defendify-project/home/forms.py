from django import forms

class searchForm(forms.Form):
    form_data = forms.CharField(label="Search" , max_length=100)


class walletForm(forms.Form):
    wallet = forms.CharField(label="Wallet", max_length=100)


class addressForm(forms.Form):
    address = forms.CharField(label="address",max_length=100)

class regexForm(forms.Form):
    regex = forms.CharField(label="",max_length=100)

class ethForm(forms.Form):
    eth_address = forms.CharField(label="eth_address",max_length=100)

class pathFinderForm(forms.Form):
    source = forms.CharField(label="source",max_length=100)
    destination = forms.CharField(label="destination",max_length=100)

class checkSanctionForm(forms.Form):
    address = forms.CharField(label="address", max_length=100)