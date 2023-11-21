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
    easy_marks = int(total_marks_req * (easy_percentage / 100))
    medium_marks = int(total_marks_req * (medium_percentage / 100))
    hard_marks = int(total_marks_req * (hard_percentage / 100))

    # Query questions from the database based on the difficulty level
    easy_questions = list(Question.objects.filter(difficulty='easy'))
    medium_questions = list(Question.objects.filter(difficulty='medium'))
    hard_questions = list(Question.objects.filter(difficulty='hard'))

    question_paper = []

    # Collecting easy questions for the question paper
    for question in easy_questions:
        if question.marks <= easy_marks:
            easy_marks -= question.marks
            question_paper.append(question)
    
    # Collecting easy questions for the question paper
    for question in medium_questions:
        if question.marks <= medium_marks:
            medium_marks -= question.marks
            question_paper.append(question)
    
    # Collecting easy questions for the question paper
    for question in hard_questions:
        if question.marks <= hard_marks:
            hard_marks -= question.marks
            question_paper.append(question)

    # Calculate the total marks of the generated question paper
    question_paper_marks = sum(question.marks for question in question_paper)

    # if question paper marks is less than required marks, then adding new extra questions to the question paper
    if question_paper_marks < total_marks_req:
        for question in (easy_questions + medium_questions + hard_questions):
            if question not in question_paper and question.marks <= total_marks_req - question_paper_marks:
                question_paper.append(question)
                question_paper_marks += question.marks

    
    serializer = QuestionSerializer(question_paper, many=True)

    return Response({
                        "question_paper": serializer.data,
                        "total_marks": question_paper_marks
                    }, status=status.HTTP_200_OK)

def homePage(request):
    return HttpResponse("Examos: A Question Paper Generator")