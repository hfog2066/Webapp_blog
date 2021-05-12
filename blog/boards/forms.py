from bootstrap_datepicker_plus import DateTimePickerInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import *


# class DateTimePicker2(DateTimePicker):
#     def render(self, name, value, attrs=None, prefix='datetimepicker2', renderer=None):
#         return DateTimePicker.render(self, name=name, value=value)

class LoginForm(AuthenticationForm):
    error_messages = AuthenticationForm.error_messages
    error_messages['invalid_login'] = ("Please enter an email and password valid.")

    username = forms.CharField(
        label='Email', required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'autofocus': 'autofocus'
            }
        )
    )
    password = forms.CharField(
        label='Password', required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        if username and CustomUser.objects.filter(username__iexact=username).exists():
            cleaned_data['username'] = cleaned_data.get('username').lower()
        return cleaned_data


class SignUpForm(UserCreationForm):
    error_messages = UserCreationForm.error_messages
    error_messages['duplicate_username'] = ("User name already exists.")

    first_name = forms.CharField(label='Name', max_length=50, required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Hector', 'autofocus': 'autofocus'}
                                 ))
    last_name = forms.CharField(label='Last name', max_length=50, required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Orozco'}
                                ))
    username = forms.CharField(label='Username', required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}
                               ))
    password1 = forms.CharField(label='Password', required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}
                                ))
    password2 = forms.CharField(label='Password check', required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}
                                ))
    email = forms.EmailField(label='Email', required=False,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Email'}
                             ))

    is_admin = forms.BooleanField(label="Are you Admin?:", required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email', 'is_admin')

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM..
        username = self.cleaned_data["username"]
        if self.instance.username == username:
            return username
        try:
            CustomUser._default_manager.get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = cleaned_data.get('username')
        if username and CustomUser.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'User name already exists.')
        elif username and not CustomUser.objects.filter(username__iexact=username).exists():
            cleaned_data['username'] = cleaned_data.get('username').lower()
        return cleaned_data


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'creation_date', 'likes')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'publication_date': DateTimePickerInput(),
            'disable_date': DateTimePickerInput(),
            'tags': forms.SelectMultiple(
                attrs={
                    'class': 'selectpicker form-control border',
                    'title': '---------',
                    'data-selected-text-format': 'count > 3',
                    'data-live-search': 'true',
                    'data-style': 'btn-secondary',
                    'data-width': '100%',
                }
            ),
            'categories': forms.SelectMultiple(
                attrs={
                    'class': 'selectpicker form-control border',
                    'title': '---------',
                    'data-selected-text-format': 'count > 3',
                    'data-live-search': 'true',
                    'data-style': 'btn-secondary',
                    'data-width': '100%',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(PostCreationForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(author=self.author, title=title).exists():
            raise forms.ValidationError("already written a post with that title.")
        return title


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'tags', 'categories', 'disable_date', 'publication_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'publication_date': DateTimePickerInput(),
            'disable_date': DateTimePickerInput(),
            'tags': forms.SelectMultiple(
                attrs={
                    'class': 'selectpicker form-control border',
                    'title': '---------',
                    'data-selected-text-format': 'count > 3',
                    'data-live-search': 'true',
                    'data-style': 'btn-secondary',
                    'data-width': '100%',
                }
            ),
            'categories': forms.SelectMultiple(
                attrs={
                    'class': 'selectpicker form-control border',
                    'title': '---------',
                    'data-selected-text-format': 'count > 3',
                    'data-live-search': 'true',
                    'data-style': 'btn-secondary',
                    'data-width': '100%',
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(author=self.author, title=title).exists():
            raise forms.ValidationError("already written a post with that title.")
        return title

class CreateCommentaryForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))
    post_id = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'type': 'hidden'}))
    class Meta:
        model = Commentary
        fields = ['text', 'post_id']