import random
from supabase_client import supabase

def get_practice_questions(rank):
    res = supabase.table("questions").select("*").execute()
    all_q = res.data
    return [q for q in all_q if rank_allowed(q["rank_required"], rank)]

def get_review_questions(user_id):
    res = supabase.table("mistakes").select("*").eq("user_id", user_id).execute()
    mistake_ids = [m["question_id"] for m in res.data]

    if not mistake_ids:
        return []

    q = supabase.table("questions").select("*").in_("id", mistake_ids).execute()
    return q.data

def get_test_questions(user_id, rank, test_count):
    if rank == "LEGEND":
        # solved の中から100問
        solved = supabase.table("solved").select("*").eq("user_id", user_id).execute().data
        solved_ids = [s["question_id"] for s in solved]
        q = supabase.table("questions").select("*").in_("id", solved_ids).execute().data
        return random.sample(q, 100)

    # 通常テスト
    practice = get_practice_questions(rank)
    return random.sample(practice, test_count)
