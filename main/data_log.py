from django.shortcuts import render

from main.models import Log, User


def log_proc(request):

    data_stack = Log.objects.select_related('user').filter(user__name=request.session['user_name'])

    print(f"data_stack: {data_stack}")

    return render(request,"LogPage.html",
                  {
                      'data_stack': data_stack,
                      'user_name': request.session['user_name']
                   })

def insert_log(request, file_name, type):
    try:
        user = User.objects.get(name=request.session['user_name'])
        Log.objects.create(user=user, file_name=file_name, type=type)
        return True
    except Exception as e:
        print(f"insert_log_error: {e}")
        return False