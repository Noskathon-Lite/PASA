import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from bettermind.models import Prof, ProfData, User, UserData

user_questions = [
    "What are you suffering from?",
    "What long you've been in this situation?",
    "Have you went to any therapist before? if yes then describe how you felt after that.",
    "Where were you mostly(schoo/college/work/home) when this started",
    "Have you told this about to anyone else?",
    "Have you tried any medications?",
    "How often do you exercise?",
    "How much you socialize?",
    "Do you do meditations?",
    "How long since you travel or went out for fun?"
    "What do you find most joyful? or what gives you sense of relief?"
    "How old are you now?"
]

user_answers = [
    "I don't know. I kind of feel sad most of the time.",
    "probably 3 months now.",
    "I'm 20.",
    "No, I haven't.",
    "My mom name is C",
    "College.",
    "No.",
    "Once in a while",
    "Not much",
    "yeah, once in a while."
    "watching movies."
    "I'm 20."
]


prof_questions = [
    "What's your expertise?",
    "Roughly, how much patients have you consulted before?",
    "Is this your first time of virtual consultation?",
    "Have you ever been in the depressing situation yourself before got out by self? if so, how long ago?",
    "Have you ever suffered from chronic anxiety?",
    "Which age patients you mostly consult with? eg: age(20 - 30)",
    "Patients with what problems have you consulted mostly? suffering from depression? or rape?",
    "Have you ever consulted teens before?",
    "Have you ever worked in some real hospitals before",
    "Do you prefer to recommend medications to patients? Yes or No?"
    "Where do you live currently?"
    "How old are you now?"
]

prof_answers = [
    "Clinical psychology. I'm a psychiatrist.",
    "around 100.",
    "Yes",
    "Yes, around a year ago.",
    "No",
    "age(25-35)",
    "Depression and chronic anxiety.",
    "Sometimes.",
    "yes.",
    "No"
    "Nepal"
    "I'm 35."
]


user1 = User.objects.get(id=14)
prof = Prof.objects.get(id=3)
userType ='p'
def createData(type):
    if type == 'p':
        print(f"Creating Prof Data of prof:{prof.username} with id: {prof.id}")
        for i in range (len(prof_questions)):
            print(f"Data Entered: {i}")
            ProfData.objects.create(prof=prof,
                    questionNo=i,
                    questionText=prof_questions[i],
                    answer=prof_answers[i]
                )
    else:
        print("Creating User Data.")
        for i in range (len(user_questions)):
            print(f"Data Entered: {i}")
            UserData.objects.create(user=user1,
            questionNo=i,
            questionText=user_questions[i],
            answer=user_answers[i]
        )
createData(userType)
# prof1 = Prof.objects.get(id=3)
# daniel = Prof.objects.get(id=2)
# for i in range(0, 10):
#     print(f"Data Entered: {i}")
#     ProfData.objects.create(prof=prof2,
#             questionNo=i,
#             questionText=questions[i],
#             answer=answers[i]
#         )
#     ProfData.objects.create(prof=daniel,
#             questionNo=i,
#             questionText=questions[i],
#             answer=answers[i]
#         )

print("DONE")