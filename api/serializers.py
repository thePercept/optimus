from rest_framework import serializers
from . models import LiveDeals
from visitor.models import DealVoucherGrabbed,UserConverted
from merchantportal.models import DealMeta
from entrypoint.models import VideoAdvertsMeta

class LiveDealsSerializers(serializers.ModelSerializer):

	class Meta:
		model = LiveDeals
		fields = '__all__'	

class DealMetaSerializer(serializers.ModelSerializer):

	class Meta:
		model = DealMeta
		fields = '__all__'

class DealVoucherGrabbedSerializer(serializers.ModelSerializer):

	class Meta:
		model = DealVoucherGrabbed
		fields = ['mobile_no','deal_id','voucher_code','voucher_status']

class AdvertSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = VideoAdvertsMeta
		fields = ['ad_video_path']	