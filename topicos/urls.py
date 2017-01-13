# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('topicos.views',
    url(r'^api/login$', 'login'),
    url(r'^api/cadastro$', 'cadastro'),
    url(r'^api/logout$', 'logout'),
    url(r'^api/whoami$', 'whoami'),
    url(r'^api/get_user_details$', 'get_user_details'),
    url(r'^api/list_topicos$', 'list_topicos'),
    url(r'^api/list_mensagens$', 'list_mensagens'),
    url(r'^api/registra_mensagem$', 'registra_mensagem'),
    url(r'^api/deleta_mensagem$', 'deleta_mensagem'),
    url(r'^api/registra_topico$', 'registra_topico'),
    url(r'^api/deleta_topico$', 'deleta_topico'),
    url(r'^api/edita_topico$', 'edita_topico'),
)
