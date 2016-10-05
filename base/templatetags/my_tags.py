from django import template
from database.models import User

register = template.Library()


# @register.inclusion_tag('header/index.html', takes_context=True)
@register.inclusion_tag('header/index.html', takes_context=True)
def header_block(context):
    request = context['request']
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        return {'user': user}
    else:
        return {'user': False}
