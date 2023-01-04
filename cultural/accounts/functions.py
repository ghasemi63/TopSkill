from django.contrib.auth.models import Group
from accounts.models import Center

"""for concatenate user privileges in user model and groups"""
"""ادغام سطح نمایش و جستجوی اطلاعات در مدل و گروه وابسته به کاربر"""


def privileges(request):
    user_id = request.user.id
    center_user = list(
        Center.objects.filter(user_to_center__id=user_id).values_list("center_title_id", flat=True))
    user_group = Group.objects.filter(user=user_id)

    def group_privilege():
        group = []
        for a in user_group:
            group += a.center.values_list("center_title_id", flat=True)
        return group

    center_user.extend(group_privilege())
    # privilege = dict.fromkeys('p', set(center_in_user))
    # print(privilege)
    return list(set(center_user))
