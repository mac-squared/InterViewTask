from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return {"users": search_users(request.args.to_dict())}, 200

def search_users(args):
    """Search users database
    
    Parameters:
        args: a dictionary containing the following search parameters:
            id: string (optional)
            name: string (optional)
            age: string (optional)
            occupation: string (optional)
    
    Returns:
        a list of users that match the search parameters, sorted by match priority
    """
    id_param = args.get("id")
    name_param = args.get("name")
    age_param = args.get("age")
    occupation_param = args.get("occupation")

    results = []

    for user in USERS:
        match_score = 0
        if id_param and user['id'] == id_param:
            match_score += 4
        if name_param and name_param.lower() in user['name'].lower():
            match_score += 3
        if age_param and int(age_param) - 1 <= user['age'] <= int(age_param) + 1:
            match_score += 2
        if occupation_param and occupation_param.lower() in user['occupation'].lower():
            match_score += 1

        if match_score > 0:
            results.append((match_score, user))

    # Sort by match score in descending order, then remove score from the results
    results.sort(key=lambda x: x[0], reverse=True)
    return [user for score, user in results]