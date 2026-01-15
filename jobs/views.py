from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from accounts.models import UserProfile
from .recommender import recommend_jobs


class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.filter(is_active=True).order_by('-posted_at')
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (permissions.IsAdminUser,)


class RecommendationsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        profile = getattr(request.user, 'profile', None)
        if not profile:
            return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        # build user text from profile fields
        parts = [profile.skills or '', profile.education or '', profile.experience or '']
        # if resume exists, we don't extract content here; see README for parsing notes
        user_text = '\n'.join(parts)

        jobs = Job.objects.filter(is_active=True).order_by('-posted_at')
        recs = recommend_jobs(user_text, list(jobs), top_n=5)
        data = [{'job': JobSerializer(job).data, 'score': score} for job, score in recs]
        return Response(data)
