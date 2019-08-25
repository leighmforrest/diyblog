from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    def clean_content(self):
        data = self.cleaned_data["content"]
        if len(data) > 1024:
            raise forms.ValidationError('The comment is too long.')
        
        return data
    