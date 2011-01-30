# -*- coding: UTF-8 -*-
from assopy import settings

from django import forms
from django import template
from django.conf import settings as dsettings
from django.core.urlresolvers import reverse

from urllib import quote_plus

register = template.Library()

_field_tpl = template.Template("""
    <div class="{{ classes|join:" " }}">
        {{ field.label_tag }}
        {{ field }}
        {{ field.errors }}
        {% if field.help_text %}<div class="help-text">{{ field.help_text }}</div>{% endif %}
    </div>
""")
@register.filter()
def field(field, cls=None):
    classes = [ 'field' ]
    if field.field.required:
        classes.append('required')
    if cls:
        classes.extend(cls.split(','))
    if isinstance(field.field.widget, (forms.HiddenInput,)):
        return str(field)
    else:
        return _field_tpl.render(template.Context(locals()))

@register.inclusion_tag('assopy/render_janrain_box.html', takes_context=True)
def render_janrain_box(context, next=None):
    if settings.JANRAIN:
        # mi salvo, nella sessione corrente, dove vuol essere rediretto
        # l'utente una volta loggato
        if next:
            context['request'].session['jr_next'] = next
        domain = settings.JANRAIN['domain']
        if not domain.endswith('/'):
            domain += '/'
        u = '%sopenid/embed?token_url=%s' % (domain, quote_plus(dsettings.DEFAULT_URL_PREFIX + reverse('assopy-janrain-token')))
    else:
        u = None
    return {
        'url': u,
    }
