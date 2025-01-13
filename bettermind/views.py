from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, ProfRegistrationSerializer, LoginSerializer, UserAnswerSubmitSerializer, ProfAnswerSubmitSerializer
from .models import User,UserData,Prof,ProfData
import json
from .utils import rank_professionals, get_summary
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .agoratoken import generate_agora_token
from django.db import transaction


@api_view(['POST'])
def get_agora_token(request):
    data = request.data
    channel_name = data.get('channel_name')
    #uid = data.get('uid', 0)  # Default is 0
    uid = data.get('uid')
    pid = data.get('pid')
    role = data.get('role', 'publisher')  # Default role

    if not channel_name:
        return Response({'error': 'Channel name is required'}, status=400)
    try:
        userToken = generate_agora_token(channel_name, uid, role)
        profToken = generate_agora_token(channel_name, pid, role)
        return Response({'token': userToken, 'channel_name': channel_name})
    
    except Exception as e:
        return Response({'error': str(e)}, status=500)


'''
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(request.body)
        if serializer.is_valid():
            user = serializer.save()
            print(f"USER Created. ID: {user.id}, Username: {user.username}")
            return Response({'msg': 'User Registered successfully.'}, status=status.HTTP_200_CREATED)
        else:
            return Response({'msg': 'User with that username already Exist.'}, status=400)
    else:
        return Response({'msg': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
'''
class UserRegistrationAPIView(APIView):
    def post(self, request):
        print("WORKED")
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"User Id is: {user.id}")
            print(f"The username is {user.username}")
            return Response({"msg": "User registered successfully", "id":user.id}, status=status.HTTP_201_CREATED)
        return Response({'msg':'User already Exist, try different username.', 'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class ProfRegistrationAPIView(APIView):
    def post(self, request):
        print("WORKED")
        serializer = ProfRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            prof = serializer.save()
            print(f"Prof Id is: {prof.id}")
            print(f"The username is {prof.username}")
            return Response({"msg": "Proffesional registered successfully", "id":prof.id}, status=status.HTTP_201_CREATED)
        #return Response({'msg':'Professional already Exist, try different username.','Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'Professional already Exist, try different username.','Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        print("THE DATA: ")
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            print(f"Logged in as: {user.username}")
            #print(f"ATTRIBUTES: {user.__dict__}") To get all attributes of an object.

            if user.user_type == 'user':
                user = User.objects.get(id=user.id)  # Cast to User
                best_profs = user.best_fit_profs.all()
                profnames = [prof.username for prof in best_profs]
                budgets = [prof.budget for prof in best_profs]
                summary = [prof.expertise for prof in best_profs]
            else:
                profnames = []
                budgets = []
                summary = []

            return Response({
                "msg": "Login successful",
                "username": user.username,
                "ID": user.id,
                "userType": "Prof" if user.user_type == "prof" else "User",
                "profnames": profnames,
                "budgets": budgets,
                "summaries": summary
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'msg': 'Invalid Username or password',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


userQuestions = [
    "How have you been feeling lately?",
    "How long has this been going on for you?",
    "Have you ever talked to a therapist or counselor before? If yes, how did it go?",
    "Did something happen recently that might have triggered how you’re feeling?",
    "Is this affecting your work, relationships, or day-to-day life?",
    "Are you taking any medications or trying anything else to help with this?",
    "What’s something you do that helps you feel even a little better?",
    "Have you gone through any big life changes lately, like a breakup, loss, or something else?",
    "Have you ever had thoughts of hurting yourself or giving up? If yes, did you talk to anyone about it?",
    "Just so we can understand better—how old are you, and how do you identify (e.g., male, female, non-binary)?",
]
profQuestions = [
    "What’s your main area of expertise (like psychology, psychiatry, or something else)?",
    "How long have you been working in mental health?",
    "Are there certain issues (like anxiety, trauma, or depression) you feel you’re best at helping with?",
    "Do you prefer working with any specific age groups, like teens, adults, or seniors?",
    "What kind of therapy do you usually use (like CBT, mindfulness, etc.)?",
    "Have you done online or virtual sessions before? How do you feel about them?",
    "Have you worked with people dealing with big issues like trauma, abuse, or major life changes?",
    "Do you work on your own or with a clinic/hospital?",
    "Have you taken any extra training, like for trauma therapy or handling anxiety?",
    "How do you usually handle it when someone is struggling with really tough thoughts or feelings, like self-harm?",
]

profData_list = []
userData_list = []
def fetch(data, Uname, p):
    data_list2 = []
    if p == True:
        for d in data:
            data_dict = {
                'prof id': d.prof.id,
                'questionNo': d.questionNo,
                'question': d.questionText,
                'answer': d.answer
            }
            data_list2.append(data_dict)
        profData_list.append(data_list2)
        
        print(f"DONE for prof: {Uname}")
    else:
        for d in data:
            data_dict = {
                'user id': d.user.id,
                'questionNo': d.questionNo,
                'question': d.questionText,
                'answer': d.answer
            }
            data_list2.append(data_dict)
        userData_list.append(data_list2)
        print(f"DONE for user: {Uname}")

def get_data(Id, p):
    if p == True:
        prof = Prof.objects.get(id=Id)
        profData = prof.profdata.all()
        uname = prof.username
        print(f"Fetching data of Prof: {uname}")
        fetch(profData, uname, p)
    else:
        user = User.objects.get(id=Id)
        userData = user.userdata.all()
        uname = user.username
        print(f"Fetching data of User: {uname}")
        fetch(userData, uname, p)
    

class UserAnswerSubmitAPIView(APIView):
    def post(self, request):
        print("INCOMING DATA: ")
        print(request.data)
        serializer = UserAnswerSubmitSerializer(data=request.data)
        print("UserAnswerSubmitAPIView triggered.")
        if serializer.is_valid():
            userId = serializer.validated_data['ID']
            answers = serializer.validated_data['answers']

            print(f"Received userId: {userId}")
            user = User.objects.get(id=userId)
            for i in range(0,10):
                UserData.objects.create(user=user, questionNo=i, questionText=userQuestions[i], answer=answers[i])
                print(f"Set answer {i} for user: {user.username}.")
            
            print("getting data of users.")
            get_data(user.id, p=False)
            prof_ids = [prof.id for prof in Prof.objects.all()]
            print("getting data of professionals.")
            for id in prof_ids:
                get_data(id, p=True)
            
            user_Jsonoutput = json.dumps(userData_list, indent=2)
            prof_Jsonoutput = json.dumps(profData_list, indent=2)
            print("Prof data: ")
            print(prof_Jsonoutput)
            print("User data: ")
            print(user_Jsonoutput)
            
            print("SENDING TO GEMINI.")
            matchingProfs = rank_professionals(user_Jsonoutput, prof_Jsonoutput)
            print(f"THE RESULT From Gemini: ")
            print(matchingProfs)
            try:
                matchingProfs_ids = [int(profId) for profId in matchingProfs.split(",")]
                matchingProfs_objects = Prof.objects.filter(id__in=matchingProfs_ids)

                with transaction.atomic() :
                    user.best_fit_profs.set(matchingProfs_objects)
                    user.save()

                matchingProfs_names = []
                matchingProfs_budgets = []
                matchingProfs_expertise = []
                for j in matchingProfs_ids:
                    object = Prof.objects.get(id=j)
                    matchingProfs_names.append(object.username)
                    matchingProfs_budgets.append(object.budget)
                    matchingProfs_expertise.append(object.expertise)

                return Response({
                    "msg": "Answers received successfully",
                    #"profId": profId,
                    "profnames": matchingProfs_names,
                    'budgets':matchingProfs_budgets,
                    'expertises':matchingProfs_expertise
                    #"answers": answers
                }, status=status.HTTP_200_OK)
            except:
                print("NO matching profs")
                return Response({
                    "msg":"No matching profs.",
                    "profnames": ""
                }, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfAnswerSubmitAPIView(APIView):
    def post(self, request):
        serializer = ProfAnswerSubmitSerializer(data=request.data)
        print("ProfAnswerSubmitAPIView triggered.")
        if serializer.is_valid():
            profId = serializer.validated_data['ID']
            answers = serializer.validated_data['answers']

            print(f"Received profId: {profId}")
            prof = Prof.objects.get(id=profId)
            for i in range(0,10):
                ProfData.objects.create(prof=prof, questionNo=i, questionText=profQuestions[i], answer=answers[i])
                print(f"Set answer {i} for prof: {prof.username}.")
            prof_data = prof.profdata.all()

            print(f"Fetching profdata of prof: {prof.username}")
            fetch(prof_data, prof.username, p=True)
            profData_list2 = profData_list.copy()
            profData_list.clear()
            prof_Jsonoutput = json.dumps(profData_list2, indent=2)

            expertise_summary = get_summary(prof_Jsonoutput)
            print(f"THE expertise of this prof is: {expertise_summary}")

            prof.expertise = expertise_summary
            prof.save()
            print(f"PROFESSIONAL EXPERTISE: {prof.expertise}")

            '''
            print("getting data of users.")
            get_data(prof.id, p=False)
            prof_ids = [prof.id for prof in Prof.objects.all()]
            print("getting data of professionals.")
            for id in prof_ids:
                get_data(id, p=True)
            
            user_Jsonoutput = json.dumps(userData_list, indent=2)
            prof_Jsonoutput = json.dumps(profData_list, indent=2)
            print("Prof data: ")
            print(prof_Jsonoutput)
            print("User data: ")
            print(user_Jsonoutput)
            
            print("SENDING TO GEMINI.")
            matchingProfs = rank_professionals(user_Jsonoutput, prof_Jsonoutput)
            print(f"THE RESULT From Gemini: ")
            print(matchingProfs)
            matchingProfs_ids = [int(profId) for profId in matchingProfs.split(",")]
            matchingProfs_names = []
            for j in matchingProfs_ids:
                object = Prof.objects.get(id=j)
                matchingProfs_names.append(object.username)
            '''
            
            return Response({
                "msg": "Answers received successfully",
                "profId": profId,
                #"usernames": matchingProfs_names,
                #"answers": answers
            }, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)