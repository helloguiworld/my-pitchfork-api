from api.models import Account
from django.db.models import Count

def get_all_accounts_ranking(max=100):
    all_accounts_ranked = (
        Account.objects
            .annotate(reviews_count=Count('reviews'))
            .filter(reviews_count__gt=0)
            .order_by('-reviews_count', 'user__date_joined')[:max]
    )
    
    all_accounts_ranking = [{
        "position": position,
        "album": account.user.username,
        "reviews_count": account.reviews_count,
    } for position, account in enumerate(all_accounts_ranked, start=1)]
    
    return all_accounts_ranking