from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    thumbs_up = forms.IntegerField(max_value=5, min_value=1, initial=1, label="")

    class Meta:
        model = models.Review
        fields = (
            "review",
            "thumbs_up",
        )
        widgets = {
            "review": forms.Textarea(attrs={"placeholder": "Review"}),
        }
        labels = {
            "review": "",
        }

    def save(self):
        review = super().save(commit=False)
        return review
