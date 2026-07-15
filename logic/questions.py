from supabase_client import supabase

def load_questions(limit_rank):
    res = supabase.table("questions").select("*").execute()
    all_q = res.data

    return [q for q in all_q if rank_allowed(q["rank_required"], limit_rank)]

def rank_allowed(required, current):
    order = ["F","E","D","C","B","A","A+","AA","S","SS","SSS","LEGEND"]
    return order.index(required) <= order.index(current)
