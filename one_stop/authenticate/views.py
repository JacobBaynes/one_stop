from django.http import response
from django.shortcuts import render
# Create your views here.


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return response.HttpResponseRedirect('')
    else:
        return render(request, "login.html", {})
