from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse

from . serializers import AdvertSerializer,LiveDealsSerializers,DealMetaSerializer,DealVoucherGrabbedSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import mixins

from entrypoint.models import RedemptionAddress,VideoAdvertsMeta
from . models import LiveDeals,MerchantDealStats
from visitor.models import DealVoucherGrabbed,UserConverted

from utils.utils_b import getVideoAdvertsMeta,getAdAccount,getDealMeta,executeRequest,checkCabletStats,getMerchantDealStatsInstance
from api.models import MerchantDealStats
# Create your views here.

class DealViewSet(ModelViewSet):
	queryset = LiveDeals.objects.all()
	serializer_class = LiveDealsSerializers



class DealView(ListAPIView):
	serializer_class = DealMetaSerializer
	

	def get_queryset(self):
		num = 0
		custom_qset = []
		objs = None

		
		#queryset = LiveDeals.objects.all()
		city_param = self.request.query_params.get('city',None)
		cablet_param = self.request.query_params.get('cablet',None)

		if city_param and cablet_param is not None:
			print("GETTING CABLET ID & CITY FROM PARAM:: ",cablet_param,city_param)

			#queryset = LiveDeals.objects.filter(city=city_param)

			if city_param == 'supercity':
				objs = LiveDeals.objects.all()
			else:
				objs= LiveDeals.objects.filter(city=city_param)

			cablet_verified_bool = checkCabletStats(cablet_param)

			if cablet_verified_bool == True:
				for deal_meta_inst in objs:
					print("DEAL META INST ::",deal_meta_inst)
					deal_id = deal_meta_inst.deal.deal_id
					cablet_id = cablet_param

					print("DEAL ID ::",deal_id)
					executed_all_stats_status = executeRequest(deal_id,cablet_id)

					if executed_all_stats_status == True:
						print(deal_meta_inst)
						custom_qset.append(getDealMeta(deal_id))
				queryset = 	custom_qset				
				return queryset						
			else:
				print("Cablet not verified")
				return  []			





class DealList(APIView):

	def get(self,request):
		deals = LiveDeals.objects.all()
		serializer = LiveDealsSerializers(deals,many=True)
		return Response(serializer.data)

	def post(self,request):
		serializer = LiveDealsSerializers(data=request.data)
		msg = "NOT VALID"
		if serializer.is_valid():
			valid_data = serializer.data
		else:
			valid_data = "SERIALIZER IS NOT VALID"
		return Response(valid_data)


@api_view(['GET','POST'])
def visitor_grabbed(request):

	if request.method == 'GET':
		print(request.query_params)
		return Response(status=status.HTTP_200_OK)


	elif request.method == 'POST':
		print("WE GOT FROM SERVER ARE",request.data)
		recieved_data = {}

		d_id = request.data['deal_id']
		merchant_deal_inst = MerchantDealStats.objects.filter(deal_id=d_id)

		recieved_data['deal_id'] = 	merchant_deal_inst
		recieved_data['voucher_code'] = request.data['voucher_code']
		recieved_data['mobile_no'] = request.data['mobile_no']
		recieved_data['voucher_status'] = "active"





		serializer = DealVoucherGrabbedSerializer(data=recieved_data)
		if serializer.is_valid():
			serializer.save()
			print(" SAVED ... AND .....PRINTING THE RECVD JSON OBJECT  :",request.data)
			#return Response(status=status.HTTP_200_OK)		
			return JsonResponse({'saved':"ok"})	
		else:
			print(serializer.errors)
			return Response(status=status.HTTP_401_UNAUTHORIZED)



class AdvertView(ListAPIView):
	serializer_class = AdvertSerializer

	def get_queryset(self):
		objs = None
		custom_qset = []

		# city_param = self.request.query_params.get('city',None)
		cablet_param = self.request.query_params.get('cablet',None)
		merchant_id = self.request.query_params.get('mid',None)

		if merchant_id and cablet_param is not None:

			objs = VideoAdvertsMeta.objects.filter(ad_acc_id=getAdAccount(merchant_id),ad_status=False)
			print(objs)
			for vid_ad_meta in objs:
				print("INSIDE LOOP API",vid_ad_meta)

				custom_qset.append(vid_ad_meta)

			queryset = custom_qset

			return queryset


