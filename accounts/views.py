from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here

def signup(request):
    if request.method == 'POST':
        # User has info and wants an account now!
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'acounts/signup.html', {'error': 'Passwords must match'})
    else:
        # User wants to enter info
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        #회원가입을 한 회원만 로그인이 가능
        #데이터베이스에서 전달받은 username과 password로 사용자가 존재하는지 판단
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        #사용자가 존재한다면 로그인
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect.'})
        #존재하지 않는다면 에러를 출력
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    #Post 방식으로 요청이 들어오면 로그아웃
    return render(request, 'accounts/signup.html')
    #그게 아니라면 signup 페이지로 보내버리기