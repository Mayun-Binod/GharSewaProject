from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from django.contrib import messages

from home.models import *


# Create your views here.
def index(request):
    services = Service.objects.all()
    return render(request, 'index.html', {'services': services})


def error(request):
    return render(request, 'error.html')


def notification():
    status = Status.objects.get(status='pending')
    new = Service_Man.objects.filter(status=status)
    count = 0
    for i in new:
        count += 1
    d = {'count': count, 'new': new}
    return d


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if name != "" and email != "" and phone != "" and content != "":
            mycontact = Contact(name=name, email=email,
                                phone=phone, content=content)
            mycontact.save()
            messages.success(
                request, 'Thank You For submitting form. We will reach you ASAP!!')

        else:
            messages.error(request, 'Please Fill Up the Form Correctly!!')

    return render(request, 'contact.html')


def handleLogin(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!!')
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('loginusername')
        password = request.POST.get('loginpass')

        user = authenticate(request, username=username, password=password)
        sign=''
        
        

        if user is not None:
            
            try:
                sign = Customer.objects.get(user=user)
            except:
                pass
                
            if sign:
                login(request, user)
                messages.success(request, 'User login successfully!')
                return redirect('index')
            
            
            else:
                stat = Status.objects.get(status = 'Accept')
                ser = False
                try:
                    ser = Service_Man.objects.get(status= stat, user=user)
                
                except:
                    pass
                
                if ser:
                    login(request, user)
                    messages.success(request, 'User login successfully!')
                    
                    return redirect('index')
                
                else:
                    messages.error(request, 'Either your request is pending or you arenot a Member')
                    return redirect('login')
            
            
                
        else:
            messages.error(
                request, 'Username and password does not match!! Please enter right credential!')
            return redirect('login')

    context = {'page': page}
    return render(request, 'login_register.html', context)

def admin_login(request):
    page = 'admin_login'
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!!')
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('logusername')
        password = request.POST.get('logpass')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            
            login(request, user)
            if user.is_staff:
                request.session['uid']= request.POST['logusername']
                return redirect('dashboard')
            else:
                return redirect('error')
        
        else:
            messages.error(
                request, 'Username and password does not match!! Please enter right credential!')
            return redirect('login')
    else:
        context = {'page': page}
        return render(request, 'login_register.html', context)
        


def admin_register(request):
    page = 'admin'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['admin_username']
        email = request.POST['admin_email']
        password1 = request.POST['pw1']
        password2 = request.POST['pw2']
        fname = request.POST['a_fname']
        lname = request.POST['a_lname']

        # Create the admin user
        user = User.objects.create_superuser(username=username.lower(
        ), email=email, password=password1, first_name=fname, last_name=lname)
        user.save()

        messages.success(request, 'Your user account has been created!! Please Login!')
        return redirect('login')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def user_register(request):
    page = 'user_register'
    if request.user.is_authenticated:
        return redirect('index')

    services = Service.objects.all()
    city = City.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        cert = request.FILES.get('cert')

        # Create the user
        if User.objects.filter(username=data['user_username']).exists():
            messages.error(request, 'Username Already Exists.')

        elif User.objects.filter(email=data['user_email']).exists():
            messages.error(request, 'Email Already Exists.')
        
        elif data['user_pass1'] != data['user_pass2']:
            messages.error(request, 'Passwords donot match with each other!!')
        
        
        else:
            user = User.objects.create_user(username=data['user_username'].lower(), email=data['user_email'], password=data['user_pass1'], first_name=data['user_fname'], last_name=data['user_lname'])
            user.save()

            service = Service.objects.get(service_id=data['service'])
            city = City.objects.get(id=data['city'])

            stat = Status.objects.get(status='pending')
            Service_Man.objects.create(
                user=user, image=image, cert=cert, phone=data['user_phone'], address=data['user_address'], service=service, city=city, experience=data['exp'], status=stat)
            messages.success(request, 'Your user account has been created!! Please Login!')
            return redirect('login')

    context = {'page': page, 'services': services, 'city': city}
    return render(request, 'login_register.html', context)


def customer_register(request):
    page = 'customer_register'
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('c_image')

        # Create the user
        if User.objects.filter(username=data['customer_username']).exists():
            messages.error(request, 'Username Already Exists.')

        elif User.objects.filter(email=data['customer_email']).exists():
            messages.error(request, 'Email Already Exists.')

        elif data['customer_pass1'] != data['customer_pass2']:
            messages.error(request, 'Passwords donot match with each other!!')
        
        else:
            customer = User.objects.create_user(
                data['customer_username'].lower(), data['customer_email'], data['customer_pass1'], first_name=data['customer_fname'], last_name=data['customer_lname'])
            customer.save()

            Customer.objects.create(user=customer,  image=image,
                                    phone=data['customer_phone'], address=data['customer_address'])
            messages.success(request, 'Your user account has been created!! Please Login!')
            return redirect('login')

    context = {'page': page}
    return render(request, 'login_register.html', context)


@login_required(login_url='login')
def handleLogout(request):
    logout(request)
    messages.success(request, 'User logout successfully!')
    return redirect('index')


def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})


def serviceView(request, myid):
    messages.success(
        request, 'What are you waiting for? --> Get your “To-Do” list ready and call us')

    service = Service.objects.filter(service_id=myid)[0]
    users = Service_Man.objects.filter(service=service)

    context = {'service': service, 'users': users}

    return render(request, 'service_view.html', context)


@login_required(login_url='login')
def addService(request):
    if not request.user.is_staff:
        return redirect('error')

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if Service.objects.filter(service_name=data['service_name']).exists():
            print('Service Already Exists.')

        else:
            service = Service.objects.create(
                service_name=data['service_name'],
                service_desc=data['service_desc'],
                image=image
            )
            messages.success(request, 'Service Added!!')
            return redirect('allservices')

    return render(request, 'add_service.html')


@login_required(login_url='login')
def profile(request):
    users = User.objects.get(id=request.user.id)

    try:
        page = False
        profile = Customer.objects.get(user=users)

    except:
        page = True
        profile = Service_Man.objects.get(user=users)

    return render(request, 'profile.html', {'profile': profile, 'page': page})


# @login_required(login_url='login')
def dashboard(request):
    if not request.session.has_key('uid'):
        messages.error(request, "Either you are not logged in or you are not authorized to access the page")
        return redirect('admin_login')
    
    dic = notification()
    services = Service.objects.all().count()
    users = Service_Man.objects.all().count()
    customers = Customer.objects.all().count()

    status = Status.objects.get(status='pending')
    new = Service_Man.objects.filter(status=status)
    count=0
    for i in new:
        count+=1
    
    cus = Customer.objects.all()
    ser = Service_Man.objects.all()
    cat = Service.objects.all()
    count1=0
    count2=0
    count3=0
    for i in cus:
        count1+=1
    for i in ser:
        count2+=1
    for i in cat:
        count3+=1
        
    context = {'count':dic['count'],'new':dic['new'], 'customer':count1, 'service_man':count2, 'service':count3, 'services': services, 'users': users, 'customers': customers}
    return render(request,'admin/dashboard.html',context)


@login_required(login_url='login')
def allServices(request):
    if not request.user.is_staff:
        return redirect('error')

    services = Service.objects.all()
    return render(request, 'admin/allservices.html', {'services': services})


@login_required(login_url='login')
def editServices(request, pid):
    if not request.user.is_staff:
        return redirect('error')

    ser = Service.objects.get(service_id=pid)

    if request.method == 'POST':
        data = request.POST
        try:
            image = request.FILES['image']
            ser.image = image
            ser.save()
        except:
            pass

        ser.service_name = data['service_name']
        ser.service_desc = data['service_desc']
        ser.save()

        messages.success(request, 'Service Updated!!')

    return render(request, 'admin/edit_services.html', {'ser': ser})


@login_required(login_url='login')
def deleteService(request, myid):
    if not request.user.is_staff:
        return redirect('error')

    service = Service.objects.get(service_id=myid)
    print(service.service_name)

    service.delete()
    messages.success(request, 'Service Deleted!')
    return redirect('allservices')


@login_required(login_url='login')
def allUsers(request):
    if not request.user.is_staff:
        return redirect('error')

    users = Service_Man.objects.all().order_by('-status')
    
    return render(request, 'admin/allusers.html', {'users': users})


@login_required(login_url='login')
def deleteUser(request, myid):
    if not request.user.is_staff:
        return redirect('error')

    users = Service_Man.objects.get(id=myid)
    user = User.objects.get(username=users)

    # To delete Service Provider
    users.delete()

    # To delete user
    user.delete()
    messages.success(request, f'{user} Deleted')
    return redirect('allusers')

@login_required(login_url='login')
def acceptUser(request, myid):
    user = Service_Man.objects.get(id=myid)
    
    stat = Status.objects.get(status='Accept')

    user.status = stat
    user.save()
    return redirect('allusers')

    

@login_required(login_url='login')
def allCustomers(request):
    if not request.user.is_staff:
        return redirect('error')

    customers = Customer.objects.all()

    return render(request, 'admin/allcustomers.html', {'customers': customers})


@login_required(login_url='login')
def deleteCustomer(request, myid):
    if not request.user.is_staff:
        return redirect('error')

    customer = Customer.objects.get(id=myid)
    user = User.objects.get(username=customer)

    # To delete user
    user.delete()
    # To delete customer
    customer.delete()

    messages.success(request, 'Customer Deleted!')
    return redirect('allcustomers')


@login_required(login_url='login')
def feedback(request):
    if not request.user.is_staff:
        return redirect('error')

    msg = Contact.objects.all()

    return render(request, 'admin/feedback.html', {'msg': msg})


@login_required(login_url='login')
def deleteFeedback(request, myid):
    if not request.user.is_staff:
        return redirect('error')

    msg = Contact.objects.get(sno=myid)
    msg.delete()
    
    messages.success(request, 'Feedback deleted successfully!')

    return redirect('feedback')


@login_required(login_url='login')
def adminProfile(request):

    if request.user.is_staff:
        user = request.user
        profile = User.objects.get(username=user)
        print(profile)
    return render(request, 'admin/admin_profile.html', {'profile': profile})


@login_required(login_url='login')
def editAdmin(request, pid):
    if not request.user.is_staff:
        return redirect('error')

    user = User.objects.get(username=request.user)
    edit = 'profile'
    if request.method == 'POST':
        username = request.POST['admin_username']
        email = request.POST['admin_email']
        fname = request.POST['a_fname']
        lname = request.POST['a_lname']

        user.username = username
        user.email = email
        user.first_name = fname
        user.last_name = lname
        # print(user.username, user.email, user.first_name, user.last_name)
        user.save()
        messages.info(request, 'Profile Updated!')
        return redirect('admin_profile')

    return render(request, 'admin/edit_admin.html', {'user': user, 'edit': edit})


@login_required(login_url='login')
def changeAdminpass(request, pid):
    if not request.user.is_staff:
        return redirect('error')

    user = User.objects.get(username=request.user)
    edit = 'pass'
    if request.method == 'POST':
        old_password = request.POST['pw']
        new_password = request.POST['pw1']
        again_password = request.POST['pw2']

        if user.check_password(old_password) == True:  # Check the old password
            if new_password == again_password:
                user.set_password(new_password)  # Change the new password
                user.save()
                messages.success(
                    request, 'Password changed successfully! Please Login Again!!')
                return redirect('index')
        else:
            messages.error(request, "Password donot match!!")
            return HttpResponseRedirect("")

    return render(request, 'admin/edit_admin.html', {'user': user, 'edit': edit})


# Edit Profile
@login_required(login_url='login')
def edit_profile(request):
    print(request.user)

    u = User.objects.get(id=request.user.id)

    try:
        page = True
        user = Service_Man.objects.get(user=u)

    except:
        page = False
        user = Customer.objects.get(user=u)

    services = Service.objects.all()
    city = City.objects.all()

    if request.method == 'POST':
        data = request.POST

        try:
            image = request.FILES['image']
            user.image = image
            user.save()
        except:
            pass

        try:
            user.experience = data['exp']
            serv = Service.objects.get(service_id=data['service'])
            ct = City.objects.get(id=data['city'])
            user.service = serv
            user.city = ct
        except:
            pass

        user.address = data['address']
        user.phone = data['phone']
        u.username = data['username']
        u.first_name = data['fname']
        u.last_name = data['lname']
        u.email = data['email']

        u.save()
        user.save()
        messages.success(request, 'Profile Updated!!')
        return redirect('profile')

    context = {'page': page, 'services': services, 'city': city, 'user': user}
    return render(request, 'editprofile.html', context)


# Customer Booking
@login_required(login_url='login')
def customerBooking(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        customer = Customer.objects.get(user=request.user)
    except:
        messages.error(request, 'You must be customer to book a service!!')
        return redirect('services')

    u = User.objects.get(id=pid)
    serv = Service_Man.objects.get(user=u)

    if request.method == 'POST':
        data = request.POST
        status = Status.objects.get(status="pending")
        book = Booking.objects.create(status=status, user=serv, customer=customer,
                                      book_date=data['date'], book_days=data['day'], book_hours=data['hour'])
        print(book)
        return redirect('booking_details')

    return render(request, 'booking.html', {'serv': serv, 'customer': customer})

# Customer Booking Details


@login_required(login_url='login')
def bookingDetails(request):
    page = True
    user = User.objects.get(id=request.user.id)
    try:
        customer = Customer.objects.get(user=user)
        books = Booking.objects.filter(
            customer=customer).order_by('-book_date')

    except:
        return redirect('user_booking')

    context = {'books': books, 'page': page}
    return render(request, 'booking_details.html', context)


# Customer Cancellation View
@login_required(login_url='login')
def cancelBooking(request, pid):
    ser = Booking.objects.get(id=pid)
    ser.delete()
    return redirect('booking_details')

# Service Provider Cancelling Booking


@login_required(login_url='login')
def spcancelBooking(request, pid):
    ser = Booking.objects.get(id=pid)
    sta = Status.objects.get(status='Reject')
    ser.status = sta
    ser.save()
    return redirect('booking_details')


# Service Provider Details
@login_required(login_url='login')
def bookingStatus(request, pid):
    book = Booking.objects.get(id=pid)
    
    return render(request, 'booking_status.html', {'book': book})


# Service Provider Booking Details
@login_required(login_url='login')
def userBooking(request):
    page = False
    user = User.objects.get(id=request.user.id)
    try:
        serv = Service_Man.objects.get(user=user)
        books = Booking.objects.filter(user=serv)

    except:
        return redirect('user_booking')

    context = {'books': books, 'page': page}
    return render(request, 'booking_details.html', context)

# Booking Confirm View


@login_required(login_url='login')
def accept_confirmation(request, pid):
    ser = Booking.objects.get(id=pid)
    sta = Status.objects.get(status='Accept')
    ser.status = sta
    ser.save()
    return redirect('booking_details')



@login_required(login_url='login')
def adminBooking(request):
    if not request.user.is_staff:
        return redirect('error')

    books = Booking.objects.all()
    return render(request, 'admin/admin_booking.html', {'books': books})


@login_required(login_url='login')
def adminCity(request):
    if not request.user.is_staff:
        return redirect('error')

    cities = City.objects.all()

    if request.method == 'POST':
        city = request.POST['city']

        if City.objects.filter(city=city).exists():
            messages.error(request, f'{city} already exists')
            return redirect('city_list')

        else:
            City.objects.create(city=city)
            messages.success(request, f'{city} Added successfully')
            return redirect('city_list')

    return render(request, 'admin/city_list.html', {'cities': cities})


@login_required(login_url='login')
def deleteCity(request, pid):
    if not request.user.is_staff:
        return redirect('error')

    city = City.objects.get(id=pid)
    city.delete()
    messages.success(request, f'{city} Deleted successfully')
    return redirect('city_list')


def search(request):
    page = True
    query = request.GET.get('search')

    if len(query) > 78:
        service = Service.objects.none()

    else:
        allServiceTitle = Service.objects.filter(service_name__icontains=query)
        allServicedesc = Service.objects.filter(service_desc__icontains=query)
        service = allServiceTitle.union(allServicedesc)

    context = {'service': service, 'query': query, 'page': page}
    return render(request, 'search.html', context)


def searchProvider(request):
    page = False
    city = City.objects.all()
    service = Service.objects.all()

    if request.method == 'POST':
        city = request.POST.get('city')
        service = request.POST.get('service')
        
        users = Service_Man.objects.filter(city=city, service=service)
        
        serv = Service.objects.get(service_id=service) #To get the service name
        ct = City.objects.get(id=city) #To get the location
        
        context = {'ct': ct, 'serv': serv,
                   'users': users, 'page': page}
        return render(request, 'search.html', context)

    context = {'city': city, 'service': service, 'page': page}
    return render(request, 'search_sp.html', context)



@login_required(login_url='login')
def user_profile(request):
    if request.user.is_staff:

        category = request.GET.get('category')

        if category == None:
            services = Service.objects.all()
            count = services.count()
            category = 'Total Services Offered'

            return render(request, 'user_profile.html', {'services': services, 'count': count, 'category': category},)

        elif category == 'users':
            users = Service_Man.objects.all()
            count = users.count()
            category = 'Total Service-Man'

            return render(request, 'user_profile.html', {'users': users, 'count': count, 'category': category})

        elif category == 'customer':
            customers = Customer.objects.all()
            count = customers.count()

            category = "Total Customers"
            return render(request, 'user_profile.html', {'customers': customers, 'count': count, 'category': category})

        else:

            return render(request, 'user_profile.html')

    else:
        return HttpResponse('Error')


@login_required(login_url='login')
def admin_home(request):
    if request.user.is_staff:
        services = Service.objects.all()
        users = Service_Man.objects.all()
        customers = Customer.objects.all()

        total_services = services.count()
        total_users = users.count()
        total_customers = customers.count()

        context = {'services': services, 'users': users, 'customers': customers,
                   'total_services': total_services, 'total_users': total_users, 'total_customers': total_customers}

        return render(request, 'admin_home.html', context)
    else:
        return redirect('error')
