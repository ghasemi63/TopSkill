from django.contrib.auth.models import Group
from accounts.models import Center


def privileges(request):
    user_id = request.user.id
    center_in_user = list(
        Center.objects.filter(user_to_center__id=user_id).values_list("center_title_id", flat=True))
    user_group = Group.objects.filter(user=user_id)

    def groups_privilege():
        group_privilege = []
        for a in user_group:
            group_privilege += a.center.values_list("center_title_id", flat=True)
        return group_privilege

    center_in_user.extend(groups_privilege())
    return center_in_user
