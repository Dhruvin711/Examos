from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer

from .models import Question

# Create your views here.

# @api_view(['GET'])
# def updateQuestionMarks(request):
#     questions = Question.objects.all()

#     for q in questions:
#         if q.difficulty == 'easy':
#             q.marks = 2
#         if q.difficulty == 'medium':
#             q.marks = 3
#         if q.difficulty == 'hard':
#             q.marks = 5
        
#         q.save()    

#     return HttpResponse("done")

@api_view(['POST'])
def createQuestion(request):
    questions = request.data

    for question_data in questions:
        if not question_data:
            return Response({"error": "Empty request payload"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the required keys exist in the JSON payload
        required_keys = ['question', 'subject', 'topic', 'difficulty', 'marks']
        if not all(key in question_data for key in required_keys):
            return Response({"error": "Incomplete question data"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = QuestionSerializer(data=question_data)
        if serializer.is_valid():
            serializer.save()
    
    return Response({"Success"})

@api_view(['GET'])
def questionStore(request):
    questions = Question.objects.all()
    serializers = QuestionSerializer(questions, many=True)

    return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def generateQuestionPaper(request):
    data = request.data

    total_marks_req = data['marks']
    easy_percentage = data['easy']
    medium_percentage = data['medium']
    hard_percentage = data['hard']

    # Calculate the marks of each difficulty level
    easy_questions_marks = int(total_marks_req * (easy_percentage / 100))
    medium_questions_marks = int(total_marks_req * (medium_percentage / 100))
    hard_questions_marks = int(total_marks_req * (hard_percentage / 100))

    # Query questions from the database based on the difficulty level
    easy_questions = list(Question.objects.filter(difficulty='easy'))
    medium_questions = list(Question.objects.filter(difficulty='medium'))
    hard_questions = list(Question.objects.filter(difficulty='hard'))

    question_paper = []

    # Collecting easy questions for the question paper
    for question in easy_questions:
        if question.marks <= easy_questions_marks:
            easy_questions_marks -= question.marks
            question_paper.append(question)

    curr_easy_marks = sum(q.marks for q in question_paper)
    
    # Collecting easy questions for the question paper
    for question in medium_questions:
        if question.marks <= medium_questions_marks:
            medium_questions_marks -= question.marks
            question_paper.append(question)

    curr_medium_marks = sum(q.marks for q in question_paper) - curr_easy_marks
    
    # Collecting easy questions for the question paper
    for question in hard_questions:
        if question.marks <= hard_questions_marks:
            hard_questions_marks -= question.marks
            question_paper.append(question)

    curr_hard_marks = sum(q.marks for q in question_paper) - curr_medium_marks - curr_easy_marks

    # Calculate the total marks of the generated question paper
    question_paper_marks = sum(question.marks for question in question_paper)

    # if question paper marks is less than required marks, then adding new extra questions to the question paper
    new_easy_questions = [q for q in easy_questions if q not in question_paper]
    new_medium_questions = [q for q in medium_questions if q not in question_paper]
    new_hard_questions = [q for q in hard_questions if q not in question_paper]

    new_easy = 0
    new_medium = 0
    new_hard = 0

    easy_marks = easy_questions[0].marks
    medium_marks = medium_questions[0].marks
    hard_marks = hard_questions[0].marks

    for x in range(len(new_easy_questions) + 1):
        for y in range(len(new_medium_questions) + 1):
            for z in range(len(new_hard_questions) + 1):
                if easy_marks*x + medium_marks*y + hard_marks*z == total_marks_req - question_paper_marks:
                    new_easy = x
                    new_medium = y
                    new_hard = z
                    break
    
    for question in new_easy_questions:
        if new_easy == 0:
            break

        question_paper.append(question)
        curr_easy_marks += question.marks
        new_easy-=1

    for question in new_medium_questions:
        if new_medium == 0:
            break
    
        question_paper.append(question)
        curr_medium_marks += question.marks
        new_medium-=1

    for question in new_hard_questions:
        if new_hard == 0:
            break
    
        question_paper.append(question)
        curr_hard_marks += question.marks
        new_hard-=1

    question_paper_marks = sum(question.marks for question in question_paper)

    final_easy_percentage = curr_easy_marks / question_paper_marks * 100
    final_medium_percentage = curr_medium_marks / question_paper_marks * 100
    final_hard_percentage = curr_hard_marks / question_paper_marks * 100

    # Serializing the question paper data
    serializer = QuestionSerializer(question_paper, many=True)

    return Response({
                        "question_paper": serializer.data,
                        "total_marks": question_paper_marks,
                        "Easy Question Percentages" : final_easy_percentage,
                        "Medium Question Percentages": final_medium_percentage,
                        "Hard Question Percentages": final_hard_percentage,
                    }, status=status.HTTP_200_OK)

def homePage(request):
    return HttpResponse("Examos: A Question Paper Generator")