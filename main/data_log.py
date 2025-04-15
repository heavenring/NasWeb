from django.shortcuts import render

from main.models import Log


def log_proc(request):

    data_stack = Log.objects.filter(user__name = request.session['user_name'])


    print(data_stack)

    return render(request,"LogPage.html", {'data_stack': data_stack})