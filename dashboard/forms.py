from django import forms

from blog.models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
    
    def clean_content(self):
        data = self.cleaned_data["content"]
        if len(data) > 3000:
            raise forms.ValidationError("The field is too long.")
        return data
    