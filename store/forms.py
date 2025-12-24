from django import forms
from .models import Contact, Review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review 
        fields = ['rating', 'comment'] 
    rating = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],
        widget=forms.RadioSelect
    
    )

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'subject', 'message']
        
        # Tùy chỉnh giao diện 
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ tên của bạn'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Nhập email'}),

            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mô tả ngắn gọn về vấn đề bạn đang gặp phải'}), 
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Mô tả chi tiết về vấn đề bạn đang gặp phải'}),
#            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
        labels = {
            'subject': 'Tiêu đề gửi', 
        }