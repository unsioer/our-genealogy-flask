from models.article import Article
from models.family import Family


def check_family_full_auth(family: Family, current_user_id, is_admin):
    if is_admin:
        return True
    if family.created_by == current_user_id:
        return True
    return False


def check_family_edit_auth(family: Family, current_user_id, is_admin):
    if is_admin:
        return True
    if current_user_id in family.admins or current_user_id == family.created_by:
        return True
    return False


def check_family_read_auth(family: Family, current_user_id, is_admin):
    if is_admin:
        return True
    if family.is_public:
        return True
    if current_user_id in family.admins or current_user_id == family.created_by or current_user_id in family.read_admins:
        return True

def check_article_like_auth(article:Article,is_admin=None,current_user_id=None):
    if article.access_level==0:
        return True
    if is_admin:
        return True
    if article.user_id==current_user_id:
        return True
    return False


