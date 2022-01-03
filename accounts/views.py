from django.shortcuts import render

def signup(request):
    errormessage = " "
    if request.method == 'GET':
        return render(request, "accounts/signup.html", {"error":errormessage})
    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password']
        password2 = request.POST['confirmpassword']

        if(password1 != password2):
            errormessage = "Password did not match"
            return render(request, "accounts/signup.html", {"error":errormessage})
        else:
            return render(request, "accounts/signup.html", {"error":errormessage})
