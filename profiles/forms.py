from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Renders all fields except for the user field
        exclude = ("user", "profile_image", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "default_phone_number": "Phone Number",
            "default_postcode": "Postal Code",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County, State or Locality",
        }

        self.fields["default_phone_number"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if field != "default_country":
                if self.fields[field].required:
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].label = False


class ProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            "profile_image",
            "default_phone_number",
            "first_name",
            "last_name"
        )
        labels = {
            "default_phone_number": "Phone number",
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )
