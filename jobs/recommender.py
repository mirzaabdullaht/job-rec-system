from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def recommend_jobs(user_text, jobs, top_n=5):
    """Return top_n jobs most similar to user_text.

    jobs: queryset or list of Job objects with `.description` attribute
    user_text: combined text from resume + skills + education + experience
    """
    job_texts = [getattr(j, 'description', '') or '' for j in jobs]
    # corpus: user_text as first document then job descriptions
    corpus = [user_text] + job_texts
    vect = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf = vect.fit_transform(corpus)
    # cosine similarity between user (index 0) and all jobs
    cosine_similarities = linear_kernel(tfidf[0:1], tfidf[1:]).flatten()
    # get top indices
    top_idx = cosine_similarities.argsort()[::-1][:top_n]
    results = []
    for idx in top_idx:
        score = float(cosine_similarities[idx])
        results.append((jobs[idx], score))
    return results
