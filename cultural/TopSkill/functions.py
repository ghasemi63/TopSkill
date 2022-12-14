from django.utils.translation import gettext_lazy as _


def td(ta):
    t = list(ta)
    if t[0] == '9':
        t[0] = '139'
    elif t[0] == '4':
        t[0] = '14'
    if t[-1] == '1':
        t[-1] = '07'
    else:
        t[-1] = '11'
    t.append('01')
    print(t)
    lists = ''.join(map(str, t))
    return lists


def toastrMessagePure(message):
    return list(message)


def toastrMessageForm(form):
    return [v for v in form.errors.values()]
