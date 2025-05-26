from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from uuid import uuid4
from config.settings import MEDIA_ROOT
from django.shortcuts import redirect
import json
from django.http import JsonResponse
from django.contrib import messages


def profile_view(request):
    return render(request, 'user/profile.html')

class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        email=request.data.get('email', None)
        password=request.data.get('password', None)

        if email is None:
            return Response(status=500, data=dict(message='이메일을 입력해주세요'))

        if password is None:
            return Response(status=500, data=dict(message="비밀번호를 입력해주세요"))

        user=User.objects.filter(email=email).first()

        if user is None:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다'))

        if user.check_password(password) is None:
            return Response(status=500, data=dict(message="비밀번호가 잘못되었습니다"))

        request.session['loginCheck']=True
        request.session['email'] = user.email

        return Response(status=200, data=dict(message='로그인 성공'))

class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        password=request.data.get('password')
        email=request.data.get('email')
        user_id=request.data.get('user_id')
        name=request.data.get('name')

        if User.objects.filter(email=email).exists():
            return Response(status=500, data=dict(message="이메일 주소가 이미 존재합니다."))
        elif User.objects.filter(user_id=user_id).exists():
            return Response(status=500, data=dict(message='사용자 이름 "'+user_id+'"이(가) 존재합니다.'))

        User.objects.create(password=make_password(password),
                            email=email,
                            user_id=user_id,
                            name=name)

        # UserPreference 생성 (1줄 추가)
        from .models import UserPreference
        UserPreference.objects.create(user=User.objects.get(email=email))

        # 세션 저장 (2줄 추가)
        request.session['loginCheck'] = True
        request.session['email'] = email

        # return 문 수정 (기존 1줄 → 새로운 1줄)
        return Response(status=200, data=dict(
            message="회원가입에 성공하였습니다. 취향을 설정해주세요.",
            redirect_to_onboarding=True
        ))

class Logout(APIView):
    def get(self, request):
        request.session.flush()  # 세션 초기화
        return redirect('/')  # 또는 로그인 페이지로 이동


def onboarding_view(request):
    if not request.session.get('loginCheck'):
        messages.error(request, '로그인이 필요합니다.')
        return redirect('/user/login/')

    if request.method == 'GET':
        user_email = request.session.get('email')
        user = User.objects.filter(email=user_email).first()

        if not user:
            return redirect('/user/login/')

        from .models import UserPreference
        preference, created = UserPreference.objects.get_or_create(user=user)

        if preference.onboarding_completed:
            messages.info(request, '이미 취향 설정이 완료되었습니다.')
            return redirect('/')

        return render(request, 'user/onboarding.html')

    elif request.method == 'POST':
        try:
            user_email = request.session.get('email')
            user = User.objects.filter(email=user_email).first()

            if not user:
                return JsonResponse({'success': False, 'message': '사용자 정보를 찾을 수 없습니다.'})

            data = json.loads(request.body)
            from .models import UserPreference
            preference, created = UserPreference.objects.get_or_create(user=user)

            # 온보딩 데이터 저장
            preference.genres = data.get('genres', [])
            preference.goals = data.get('goals', [])
            preference.reading_time = data.get('readingTime', '')
            preference.reading_duration = data.get('readingDuration', '')
            preference.reading_complexity = data.get('readingComplexity', '')
            preference.favorite_books = data.get('favoriteBooks', [])
            preference.mood = data.get('mood', [])
            preference.onboarding_completed = True
            preference.save()

            return JsonResponse({
                'success': True,
                'message': '취향 설정이 완료되었습니다!',
                'redirect_url': '/'
            })

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'저장 중 오류가 발생했습니다: {str(e)}'})


def skip_onboarding_view(request):
    if not request.session.get('loginCheck'):
        return redirect('/user/login/')

    user_email = request.session.get('email')
    user = User.objects.filter(email=user_email).first()

    if user:
        from .models import UserPreference
        preference, created = UserPreference.objects.get_or_create(user=user)
        preference.onboarding_completed = True
        preference.save()
        messages.info(request, '나중에 설정에서 취향을 설정할 수 있습니다.')

    return redirect('/')