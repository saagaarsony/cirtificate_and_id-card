from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect, render,get_object_or_404
from .models import UserProfile
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserProfileSerializer

def index(request):
    return render(request,'index.html')

def form(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        surname = request.POST.get('surname', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        registration_no = request.POST.get('registration_no', '')
        address = request.POST.get('address', '')
        pincode = request.POST.get('pincode', '')
        date_of_birth = request.POST.get('date_of_birth', '')
        title = request.POST.get('title', '')
        pimage = request.FILES.get('pimage', None)

        if not all([first_name, surname, email, phone, registration_no, address, pincode, date_of_birth, title, pimage]):
            # Handle the case when some required fields are not present
            return HttpResponse("Some required fields are missing.")
        u_profile = UserProfile(
            first_name=first_name,
            surname=surname,
            email=email,
            phone=phone,
            registration_no=registration_no,
            address=address,
            pincode=pincode,
            date_of_birth=date_of_birth,
            title=title,
            pimage=pimage
        )
        u_profile.save()

        # Redirect to the detail view with the user's ID
        return redirect('user_detail', user_id=u_profile.id)

    return render(request, 'form.html')

def update_form(request, user_id):
    try:
        user_profile = get_object_or_404(UserProfile, id=user_id)
    except UserProfile.MultipleObjectsReturned:
        return HttpResponseServerError("Multiple user profiles with the same ID. Contact the administrator.")

    if request.method == "POST":
        # Update other fields
        user_profile.first_name = request.POST['first_name']
        user_profile.surname = request.POST['surname']
        user_profile.email = request.POST['email']
        user_profile.phone = request.POST['phone']
        user_profile.registration_no = request.POST['registration_no']
        user_profile.address = request.POST['address']
        user_profile.pincode = request.POST['pincode']
        user_profile.date_of_birth = request.POST['date_of_birth']
        user_profile.title = request.POST['title']

        # Handle image update
        new_image = request.FILES.get('pimage', None)
        if new_image:
            # Delete the old image (optional, depends on your requirements)
            user_profile.pimage.delete(save=True)

            # Save the new image
            user_profile.pimage = new_image

        user_profile.save()

        return redirect('user_detail', user_id=user_profile.id)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'update.html', context)



def delete_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)

    if request.method == "POST":
        user_profile.delete()
        return redirect('all')  # Redirect to the desired page after deletion

    return render(request, 'delete_confirmation.html', {'user_profile': user_profile})

def user_detail(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'detail.html', context)

# That IS For All Users List
def all_users(request):
    user_profiles = UserProfile.objects.all()

    context = {
        'user_profiles': user_profiles,
    }

    return render(request, 'all.html', context)

# For IdCard Builder
def user_id(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'idcard.html', context)

class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_url_kwarg = 'user_id'