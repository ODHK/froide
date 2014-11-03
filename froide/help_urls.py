from django.conf import settings
from django.conf.urls import patterns
from django.shortcuts import render
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.utils.translation import ugettext as _


def help_view(request, template=None, language=None):
    language = language or getattr(request, 'LANGUAGE_CODE',
                                   settings.LANGUAGE_CODE)
    template_name = 'help/{}/{}'.format(language, template)
    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        pass
    if len(language) > 2:
        return help_view(request, template=template, language=language[:2])
    if not settings.LANGUAGE_CODE.startswith(language):
        return help_view(request, template=template,
                         language=settings.LANGUAGE_CODE)
    raise Http404


urlpatterns = patterns("",
    (r'^$', help_view, {'template': 'index.html'}, 'help-index'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('about'), help_view, {'template': 'about.html'},
        'help-about'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('terms'), help_view, {'template': 'terms.html'},
        'help-terms'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('privacy'), help_view, {'template': 'privacy.html'},
        'help-privacy'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('making-requests'), help_view,
        {'template': 'making-requests.html'}, 'help-making_requests'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('your-privacy'), help_view,
        {'template': 'your-privacy.html'}, 'help-your_privacy'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('for-ai-officers'), help_view,
        {'template': 'ai-officers.html'}, 'help-ai_officers'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('unhappy'), help_view,
        {'template': 'unhappy.html'}, 'help-unhappy'),
    (r'^%s/$' % _('donate'), help_view, {'template': 'donate.html'},
        'help-donate'),
)
