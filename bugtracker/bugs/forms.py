from django import forms

class BugForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    status = forms.ChoiceField(choices=[("OPEN", "Open"), ("IN_PROGRESS", "In Progress"), ("CLOSED", "Closed")])
    priority = forms.ChoiceField(choices=[("LOW", "Low"), ("MEDIUM", "Medium"), ("HIGH", "High")])
    screenshot = forms.ImageField(required=False)
    assigned_to = forms.IntegerField(required=False)

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField()
#     class Meta:
#         model = User
#         fields = ("username","email","password1","password2")


    
