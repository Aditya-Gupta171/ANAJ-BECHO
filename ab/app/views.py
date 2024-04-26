import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from . models import UserData,Products
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    return render(request,"home.html")

def products(request):
    instance=Products.objects.all()
    productsArray=[]
    for obj in instance:
        tempObj={'name':obj.name,'description':obj.description,'price':obj.price,'image':obj.pImage.url,'product_id':obj.id}
        productsArray.append(tempObj)

    return render(request,'product.html',{'productInstance':productsArray})

def cart(request):
        if(request.session.get('isloggedIn')):
         instance=UserData.objects.get(email=request.session.get('emailInf'))
         cartItems=instance.cartItems
         total=0
         count=0
         cartList=[]
         for items in cartItems:
            count+=1
            prod=Products.objects.filter(id=int(items))
            for obj in prod:

                tempObj={'name':obj.name,'description':obj.description,'price':obj.price,'image':obj.pImage.url,'product_id':obj.id,'quantity':cartItems.get(str(items))}
                cartList.append(tempObj)
                total=total+int(cartItems.get(str(items)))*obj.price
         
         return render(request,'cart.html',{'instance':instance,'cartList':cartList,'total':total,'count':count})
        else:
            return render(request,'cart.html')

def account(request):
    if(request.session.get('isloggedIn')):
        instance=UserData.objects.get(email=request.session.get('emailInf'))
        return render(request,'account.html',{'instance':instance})
    else:
        return redirect('signup')

def aboutUs(request):
    return render(request,'aboutUs.html')


def signUp(request):
    if(request.method=="POST"):
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        if(UserData.objects.filter(email=email).exists()):
            return render(request,'signup.html',{'message':"Already Existing User"})
        else:
            newUser=UserData(name=name,email=email,password=password)
            newUser.save()
            return redirect('login')

    return render(request,'signup.html')

def login(request):
    if(request.method=="POST"):
        email=request.POST.get('email')
        password=request.POST.get('password')
        if(UserData.objects.filter(email=email, password=password).exists()):
            request.session['isloggedIn']=True
            request.session['emailInf']=email
            return redirect('home')
        else:
            return render(request,'login.html',{'message':"invalid credentials"})

    return render(request,'login.html')  


def logout(request):
    request.session.clear()
    return redirect('home')


@csrf_exempt
def addToCart(request):
    if(request.method=="POST"):
        pId=str((json.loads(request.body)).get('pId'))
        print(pId)

        instance=get_object_or_404(UserData,email=request.session.get('emailInf'))
        baseObj=instance.cartItems
        print('ini: ',baseObj)
        if(baseObj.get(pId)):
            print('thaa')
            print('dbs',baseObj.get(pId))
            baseObj[pId]=baseObj.get(pId)+1
        else:
            print('nahi tha')
            baseObj[pId]=1

        print('final: ',baseObj)

        instance.cartItems=baseObj
        instance.save()
    return JsonResponse({'message':'Product Added successfully'})    
    