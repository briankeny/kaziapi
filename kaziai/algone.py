from jobs.models import UserJobPostInteraction,JobPost
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

class JobRecommendationExtra:
    def __init__(self, user_id):
        self.user_id = user_id
        self.recommended_jobs = []

    def recommended(self):
        # Get user interactions (filtered for the user)
        user_interactions = UserJobPostInteraction.objects.filter(user=self.user_id)

        # Create user-job matrix (filtered for current user)
        user_job_matrix = csr_matrix(
            (
                [1 for _ in user_interactions], 
                ([interaction.user_id for interaction in user_interactions],
                 [interaction.jobpost_id for interaction in user_interactions])
            ),
            shape=(1, len(JobPost.objects.all()))  # One row for the current user
        )

        

        # Calculate user similarities
        user_similarities = cosine_similarity(user_job_matrix)

        # Find similar users
        similar_users = user_similarities.argsort()[:-1][::-1]

        # Recommend jobs based on similar users
        jobs_ids = []
        for similar_user in similar_users:
            jobs_ids.extend(UserJobPostInteraction.objects.filter(user=similar_user).values_list('jobpost_id', flat=True))

        self.recommended_jobs = JobPost.objects.filter(post_id__in=jobs_ids).distinct()

        return self.recommended_jobs