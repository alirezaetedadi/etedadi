
from django.http import JsonResponse, Http404, HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from api.models import customer, contact, product
from datetime import datetime


Html = "<h1 style='color:red;text-align:center;padding-top:100px'> ALIREZA ETEDADI</h1>"

@csrf_exempt
def Register(request):
    if request.method == 'POST':
        req = request.POST
        # action:create_customer - id:user_id - name:name - inviter:user_id - digits:digits - contact_id:0/1/2
        if req['action'] == 'create_customer':
            # not empty
            a = condition(['id', 'name', 'inviter', 'digits'], req)
            if a[1]:
                result = {}
                if not customer.objects.filter(user_id=req['id']).exists():

                    try:
                        inviter = customer.objects.get(user_id=req['inviter'])
                    except customer.DoesNotExist:
                        inviter = customer.objects.get(user_id='0000')


                #     create customer
                    new_customer = customer(user_id=req['id'],
                                            name=req['name'],
                                            digits=req['digits'],
                                            inviter=inviter,
                                            contact_by=contact.objects.get(app_id=req['contact_id']))
                    new_customer.save()
                    result = {'result': 'customer created'}
                else:
                    result = {'result': 'id is already exists'}
                return JsonResponse(result)
            else:
                return JsonResponse(a[0])
    else:
        return HttpResponse(Html)


@csrf_exempt
def QRcodeScanner(request):
    if request.method == 'POST':
        req = request.POST
        # action:get_inviter - qrcode:user_id
        if req['action'] == 'get_inviter':
            if not req['qrcode'] == '':
                try:
                    inviter = customer.objects.get(user_id=req['qrcode'])
                    json = {'result': inviter.name}
                    return JsonResponse(json)
                except customer.DoesNotExist:
                    json ={'result':'user not found'}
                    return JsonResponse(json)
    else:
        return HttpResponse(Html)


@csrf_exempt
def editcustomer(request):
    if request.method == 'POST':
        req = request.POST
        # action:get_customer - id:user_id
        if req['action'] == 'get_customer':
            try:
                find = customer.objects.get(user_id=req['id'])

                json = {'result': 'get_customer',
                        'id': find.user_id,
                        'name': find.name,
                        'inviter_name': find.inviter.name,
                        'inviter_id': find.inviter.user_id,
                        'digits': find.digits,
                        'contact': find.contact_by.app_id}
                return JsonResponse(json)
            except customer.DoesNotExist:
                json = {'result': 'User Not Found'}
                return JsonResponse(json)
        # action:edit_customer - id:user_id - name:name - inviter:user_id - digits:digits - contact_by:0/1/2
        elif req['action'] == 'edit_customer':
            try:
                find = customer.objects.get(user_id=req['id'])
                find.name = req['name']
                find.inviter = customer.objects.get(user_id=req['inviter'])
                find.digits = req['digits']
                find.contact_by = contact.objects.get(app_id=req['contact_by'])
                find.save()
                return JsonResponse({'result': 'Edit Customer'})
            except customer.DoesNotExist:
                json = {'result': 'Error'}
                return JsonResponse(json)
        elif req['action'] == 'del_customer':
            find = customer.objects.get(user_id=req['id'])
            find.delete()
            json = {'result': 'Customer Deleted'}
            return JsonResponse(json)
    else:
        return HttpResponse(Html)



@csrf_exempt
def viewcustomer(requset):
    list_customers = []
    req = requset.POST
    if requset.method == 'POST':
        # action:get_customers
        if req['action'] == 'get_customers':
            customers = customer.objects.all().order_by('user_id')[:]
            for i in customers:
                list_customers.append({'id': i.user_id, 'name': i.name, 'digit': i.digits, 'id2':i.id})
            json = {'result': True, 'customers': list_customers}
            return JsonResponse(json, safe=False)
    else:
        return HttpResponse(Html)

@csrf_exempt
def buy(request):
    req = request.POST
    Discount = 0
    Full_discount = 0
    if request.method == 'POST':
        if req['action'] == 'id':
            if req['part'] == '1':
                Customer = customer.objects.get(user_id=req['customer'])
                discounts = product.objects.filter(inviter_id=Customer, use=False)
                for i in discounts:
                    Discount += float(i.discount)
                json = {'customer_name':Customer.name,
                        'customer_discount':Discount,
                        'inviter_name': Customer.inviter.name,
                        'inviter_id':Customer.inviter.user_id,
                        'inviter_contact':Customer.inviter.contact_by.app_id,
                        'inviter_digits':Customer.inviter.digits}
                return JsonResponse(json)
            elif req['part'] == '2':
                Customer = customer.objects.get(user_id=req['customer'])
                discounts = product.objects.filter(inviter_id=Customer)
                if req['discount_mode'] == 'on':
                    for i in discounts:
                        i.use = True
                        i.save()
                discount = float(req['price']) * 0.05
                buy = product.objects.create(time=datetime.now(),
                                             user_id=Customer,
                                             inviter_id=Customer.inviter,
                                             price=req['price'],
                                             discount=discount)
                buy.save()
                full_discounts = product.objects.filter(inviter_id=Customer.inviter, use=False)
                for i in full_discounts:
                    Full_discount += float(i.discount)
                json = {'inviter_discount': Full_discount}
                return JsonResponse(json)

        elif req['action'] == 'gift_id':
            if req['part'] == '1':
                inviter = customer.objects.get(user_id=req['inviter'])
                json = {'inviter_name': inviter.name,
                        'inviter_contact': inviter.contact_by.app_id,
                        'inviter_digits': inviter.digits}
                return JsonResponse(json)
            elif req['part'] == '2':
                inviter = customer.objects.get(user_id=req['inviter'])
                discount = float(req['price'])*0.05
                if req['customer'] == '':
                    buy = product.objects.create(time=datetime.now(),
                                                 inviter_id=inviter,
                                                 price=req['price'],
                                                 discount=discount,
                                                 gift_d=True)
                    buy.save()
                elif req['customer'] != '':
                    buy = product.objects.create(time=datetime.now(),
                                                 user_id=customer.objects.get(user_id=req['customer']),
                                                 inviter_id=inviter,
                                                 price=req['price'],
                                                 discount=discount,
                                                 gift_d=True)
                    buy.save()
                full_discounts = product.objects.filter(inviter_id=inviter, use=False)
                for i in full_discounts:
                    Full_discount += float(i.discount)
                json = {'inviter_discount': Full_discount}
                return JsonResponse(json)

def condition(array, req):
    result = True
    message = []
    for i in array:
        if req[i] == "":
            result = False
            message.append(i)
    return {'result': str(message).replace('[', '').replace(']', '')+' are empoty'}, result

