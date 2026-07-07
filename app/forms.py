from django.forms import ModelForm, Form
from app.models import Comment, Order
class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('id','product','parent',)


class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)
