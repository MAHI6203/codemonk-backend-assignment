from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics,status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .tasks import process_paragraph_text
from .serializers import UserRegistrationSerializer,ParagraphSerializer
from .models import WordFrequency

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) 
    serializer_class = UserRegistrationSerializer

class ParagraphSubmissionView(APIView):
    """
    API endpoint for a logged-in user to submit paragraphs.
    """
    permission_classes = [IsAuthenticated] # Only logged-in users can access

    def post(self, request, *args, **kwargs):
        serializer = ParagraphSerializer(data=request.data)
        if serializer.is_valid():
            paragraphs = serializer.validated_data['paragraphs']
            for p_content in paragraphs:
                # For each paragraph, start a new background task
                process_paragraph_text.delay(request.user.id, p_content)

            return Response(
                {"message": "Your paragraphs have been submitted for processing."},
                status=status.HTTP_202_ACCEPTED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WordSearchView(APIView):
    """
    API endpoint to search for a word and get top 10 paragraphs.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        search_word = request.query_params.get('word', None)
        if not search_word:
            return Response({"error": "A 'word' query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Query the WordFrequency model to find the top 10 paragraphs for this user and word
        word_frequencies = WordFrequency.objects.filter(
            user=request.user,
            word=search_word.lower()
        ).order_by('-frequency')[:10]

        # Get the actual content of the paragraphs
        results = [wf.paragraph.content for wf in word_frequencies]

        return Response(results, status=status.HTTP_200_OK)

