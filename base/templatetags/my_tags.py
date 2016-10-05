from django import template
from database.models import User

register = template.Library()


@register.inclusion_tag('base/index.html', takes_context=True)
# @register.inclusion_tag('header/index.html')
# @register.inclusion_tag()
def say_hello(context):
    # request = context['request']
    # print request
    # user_id = request.session['user_id']
    # user = User.objects.get(id=user_id)

    # name = user.name + " " + user.lastName
    return {'name': 'wow'}
