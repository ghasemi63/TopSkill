from django.contrib.auth.models import Group


def privileges(request):
    user_id = request.user.id
    user_group = Group.objects.filter(user=user_id)
    privilege = list([a.center.values("center_title_id") for a in user_group])
    return privilege

