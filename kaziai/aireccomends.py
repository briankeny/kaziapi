from jobs.models import UserJobPostInteraction, JobPost
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

class JobRecommendation:
    def __init__(self, user_id):
        self.user_id = user_id
        self.recommended_jobs = []

    def recommend(self, top_n=5):
        try:
            # Step 1: Get all user-job interactions
            interactions = UserJobPostInteraction.objects.all()
            
            # Step 2: Create the user-job interaction matrix
            user_ids = list(set(interaction.user_id for interaction in interactions))
            jobpost_ids = list(set(interaction.jobpost_id for interaction in interactions))

            # Create a mapping from user/job IDs to indices
            user_index = {user_id: idx for idx, user_id in enumerate(user_ids)}
            job_index = {jobpost_id: idx for idx, jobpost_id in enumerate(jobpost_ids)}

            # Create a sparse matrix where rows are users and columns are job posts
            data = []
            rows = []
            cols = []
            
            for interaction in interactions:
                data.append(1)  # Indicates interaction (e.g., viewed)
                rows.append(user_index[interaction.user_id])
                cols.append(job_index[interaction.jobpost_id])
            
            user_job_matrix = csr_matrix((data, (rows, cols)), shape=(len(user_ids), len(jobpost_ids)))

            # Step 3: Calculate cosine similarity between users
            user_similarities = cosine_similarity(user_job_matrix)

            # Step 4: Get the most similar users
            similar_users = user_similarities[user_index[self.user_id]].argsort()[:-top_n-1:-1]

            # Step 5: Collect job recommendations from similar users
            recommended_job_ids = set()
            for similar_user_idx in similar_users:
                similar_user_id = user_ids[similar_user_idx]
                job_ids_for_similar_user = UserJobPostInteraction.objects.filter(user=similar_user_id).values_list('jobpost_id', flat=True)
                recommended_job_ids.update(job_ids_for_similar_user)
            
            # Step 6: Filter out jobs the current user has already interacted with
            user_job_ids = set(UserJobPostInteraction.objects.filter(user=self.user_id).values_list('jobpost_id', flat=True))
            recommended_job_ids -= user_job_ids

            # Step 7: Get the recommended job posts based on the job IDs
            self.recommended_jobs = JobPost.objects.filter(post_id__in=recommended_job_ids).distinct()

            return self.recommended_jobs
        
        except Exception as e:
            print(f'Encountered error {str(e)}')
            return []