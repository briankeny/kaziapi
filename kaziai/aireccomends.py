from jobs.models import UserJobPostInteraction, JobPost, User
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

class JobRecommendation:
    def __init__(self, user_id):
        self.user_id = user_id
        self.recommended_jobs = []

    def recommend(self, top_n=5):
        try:
            # Step 1: Fetch all user-job interactions
            all_interactions = UserJobPostInteraction.objects.all()

            # Step 2: Get list of all unique users and job posts
            all_users = User.objects.values_list('id', flat=True)
            all_jobs = JobPost.objects.values_list('post_id', flat=True)

            # Create mappings from user_id and job_id to matrix indices
            user_id_to_index = {user_id: idx for idx, user_id in enumerate(all_users)}
            job_id_to_index = {job_id: idx for idx, job_id in enumerate(all_jobs)}

            # Step 3: Build the user-job interaction matrix
            row_indices = []
            col_indices = []
            data = []
            for interaction in all_interactions:
                row = user_id_to_index.get(interaction.user_id)
                col = job_id_to_index.get(interaction.jobpost_id)
                if row is not None and col is not None:
                    row_indices.append(row)
                    col_indices.append(col)
                    data.append(1)  # You can adjust this to represent interaction strength

            user_job_matrix = csr_matrix(
                (data, (row_indices, col_indices)),
                shape=(len(all_users), len(all_jobs))
            )

            # Step 4: Identify the index of the current user
            current_user_index = user_id_to_index.get(self.user_id)
            if current_user_index is None:
                print(f"User ID {self.user_id} not found.")
                return []

            # Step 5: Calculate cosine similarity between the current user and all other users
            user_similarities = cosine_similarity(user_job_matrix[current_user_index], user_job_matrix).flatten()

            # Step 6: Identify top N similar users (excluding the current user)
            similar_user_indices = user_similarities.argsort()[-top_n-1:-1][::-1]
            similar_users = [all_users[idx] for idx in similar_user_indices]

            # Step 7: Fetch jobs interacted by similar users that the current user hasn't interacted with
            current_user_jobs = UserJobPostInteraction.objects.filter(user_id=self.user_id).values_list('jobpost_id', flat=True)
            similar_users_jobs = UserJobPostInteraction.objects.filter(user_id__in=similar_users).exclude(jobpost_id__in=current_user_jobs).values_list('jobpost_id', flat=True)

            # Step 8: Count the frequency of each job in similar users' interactions
            job_counter = Counter(similar_users_jobs)
            recommended_job_ids = [job_id for job_id, _ in job_counter.most_common(top_n)]

            # Step 9: Fetch the JobPost objects for the recommended job IDs
            self.recommended_jobs = JobPost.objects.filter(post_id__in=recommended_job_ids)
            return self.recommended_jobs
    
        except Exception as e:
            print(f'Reccommendation encountered an error {e}')
            return []