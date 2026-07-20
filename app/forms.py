from django import forms
from app.models import Comment, Order, Product

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('id', 'product', 'parent',)


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)


class ProductModelForm(forms.ModelForm):  
    class Meta:
        model = Product
        exclude = ('id', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
