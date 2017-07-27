from rest_framework import serializers
from .models import ViewData

from view.serializers import ViewDataSerializer


# class ViewDataSerializerPlus(ViewDataSerializer):
#
#     def __init__(self, *args, **kwargs):
#         super(ViewDataSerializer, self).__init__(*args, **kwargs)
#
#     # my_field = serializers.SerializerMethodField('successful_submit')
#     # def successful_submit(self, success):
#     #     return success == 1
#     image_list = serializers.ListField(source='get_image_list')
#     labels = serializers.ListField(source='get_labels')
#
#     class Meta:
#         model = ViewData
#         fields = ('image_list', 'labels', 'name')
#         read_only_fields = ('image_list',)