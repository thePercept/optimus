import json
from django.shortcuts import render
from . utils_a import getLoggedInMerchantId,getMerchantInstance,getInventoryPaginated,saveInventoryItem
#from querystring_parser import parser
# Create your views here.
def ex_index(request):
    merchant_id = getLoggedInMerchantId(request=request)
    merchant_obj = getMerchantInstance(merchant_id=merchant_id)
    merchant_category = merchant_obj.merchant_category
    inv_tools =getInventoryPaginated(merchant_id=merchant_id,request=request)
    inv_objs = inv_tools[0]
    inv_all = inv_tools[1]

    return render(request,'example/index.html',{'merchant_obj':merchant_obj,'inv_all':inv_all,'inventory_obj':inv_objs,'merchant_category':merchant_category})

def ex_ajax(request):
    print("Inside ajax view function")
    if request.is_ajax():
        lixt =[]
        if request.method == 'GET':
            print("LETS DUMP THE DATA NOW!!")
            json_data=request.GET
            print(json_data)

            for i in json_data:
                lixt = i
            print(len(lixt))
            xyz = json.loads(lixt)
            print (xyz)
            print(len(xyz))
            saveInventoryItem(xyz)
            print(xyz[0])



            #print(json_data)

    return render(request,'example/ajax.html')
