from supabase_client import supabase

def load_profile(user_id):
    res = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
    if res.data:
        return res.data[0]

    profile = {
        "user_id": user_id,
        "score": 0,
        "max_combo": 0,
        "rank": "F",
        "title": None,
        "unlocked_questions": 10,
        "test_question_count": 5,
        "legend_flag": False
    }
    supabase.table("profiles").insert(profile).execute()
    return profile

def save_profile(profile):
    supabase.table("profiles").update(profile).eq("user_id", profile["user_id"]).execute()
