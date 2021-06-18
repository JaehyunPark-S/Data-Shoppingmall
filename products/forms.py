from django import forms
from . import models


class SearchForm(forms.Form):

    name = forms.CharField(initial="Anything")
    product_type = forms.ModelChoiceField(
        required=False,
        empty_label="Any kind",
        queryset=models.ProductType.objects.all(),
    )
    product_language = forms.ModelChoiceField(
        required=False,
        empty_label="Any kind",
        queryset=models.ProductLanguage.objects.all(),
    )
    price = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ("caption", "file")

    def save(self, pk, *args, **kwargs):
        photo = super().save(commit=False)
        product = models.Product.objects.get(pk=pk)
        photo.product = product
        photo.save()


class CreateProductForm(forms.ModelForm):

    price = forms.IntegerField(initial=0)

    class Meta:
        model = models.Product
        fields = (
            "name",
            "description",
            "price",
            "upload_file",
            "filename",
            "product_type",
            "product_language",
        )
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Product Name"}),
            "description": forms.TextInput(attrs={"placeholder": "Description"}),
            "filename": forms.TextInput(attrs={"placeholder": "Filename"}),
        }

    def save(self, *args, **kwargs):
        product = super().save(commit=False)
        return product
