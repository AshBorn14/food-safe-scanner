from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import Preferences
from django.utils.html import format_html


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your Username','class':'form-control mt-1'}))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'placeholder':'Your password','class':'form-control mt-1'}))


class SignUpForm(UserCreationForm):
    """ email = forms.EmailField(label="Email address",widget=forms.TextInput(attrs={'class':'form-control'})) """
    class Meta:
        model = User
        fields = ('username', 'email' ,'password1','password2')

    username = forms.CharField(help_text='<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>',widget=forms.TextInput(attrs={'placeholder':'Your Username','class':'form-control mt-1'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Your Email id','class':'form-control mt-1'}))
    password1 = forms.CharField(help_text ='<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>',label="Password",widget=forms.PasswordInput(attrs={'placeholder':'password','class':'form-control mt-1'}))
    password2 = forms.CharField(help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>',label="Confirm Password",widget=forms.PasswordInput(attrs={'placeholder':'enter password again','class':'form-control mt-1'}))

widget_attrs={
    'class':'form-check form-check-label d-flex justify-content-between flex-wrap border border-1 rounded-3 border-dark-subtle px-3'
}

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = [
            'nutri_score_weight',
            'vegetarian_weight',
            'vegan_weight',
            'palm_oil_free_weight',
            'eco_score_weight',
            'nova_group_weight',
            'additives_weight',
            'gluten_weight',
            'milk_weight',
            'nuts_weight',
            'peanuts_weight',
            'soybeans_weight',
            
        ]
    
    WEIGHT_CHOICES = [
        (0, 'Not Important'),
        (1, 'Important'),
        (2, 'Very Important'),
        (3, 'Mandatory'),
    ]

    nutri_score_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                           widget=forms.RadioSelect(attrs=widget_attrs),
                                           label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">Good Nutritional quality (Nutri-Score)</span>')
                                           )
    
    vegetarian_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                          widget=forms.RadioSelect(attrs=widget_attrs),
                                          label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">Vegetarian</span>')
                                          )
    vegan_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                     widget=forms.RadioSelect(attrs=widget_attrs),
                                     label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">Vegan</span>')
                                     )
    palm_oil_free_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                             widget=forms.RadioSelect(attrs=widget_attrs),
                                             label=format_html('<span class="mb-0 fs-5 fw-semibold mt-2">Palm Oil Free</span>')
                                             )
    eco_score_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                         widget=forms.RadioSelect(attrs=widget_attrs),
                                         label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">Low Environment Impact (Eco-Score)</span>')
                                         )
    nova_group_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                          widget=forms.RadioSelect(attrs=widget_attrs),
                                          label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">No or little Food Processing (NOVA grpup)</span>')
                                          )
    gluten_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                      widget=forms.RadioSelect(attrs=widget_attrs),
                                      label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">Without Gluten</span>')
                                      )
    milk_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                    widget=forms.RadioSelect(attrs=widget_attrs),
                                    label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">Without Milk</span>')
                                    )
    nuts_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                    widget=forms.RadioSelect(attrs=widget_attrs),
                                    label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">Without Nuts</span>')
                                    )
    peanuts_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                       widget=forms.RadioSelect(attrs=widget_attrs),
                                       label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">Without Peanuts</span>')
                                       )
    soybeans_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                        widget=forms.RadioSelect(attrs=widget_attrs),
                                        label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">Without Soybeans</span>')
                                        )
    additives_weight = forms.ChoiceField(choices=WEIGHT_CHOICES, 
                                         widget=forms.RadioSelect(attrs=widget_attrs),
                                         label=format_html('<span class="mb-0 fs-5 fw-semibold mt-1">No or few additives</span>')
                                         )
    

