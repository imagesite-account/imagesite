from rest_framework import serializers
from .models import ViewData


class ViewDataSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(ViewDataSerializer, self).__init__(*args, **kwargs)

    # my_field = serializers.SerializerMethodField('successful_submit')
    # def successful_submit(self, success):
    #     return success == 1

    class Meta:
        model = ViewData
        fields = '__all__'
