import json
import logging
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from topicos.models import Topico
from topicos.models import Mensagem
from topicos.decorators import ajax_login_required
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    user_dict = None

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            user_dict = _user2dict(user)
    return HttpResponse(json.dumps(user_dict), content_type='application/json')


def cadastro(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    first_name = request.POST['first_name']
    is_superuser = json.loads(request.POST['is_superuser'])

    user_dict = adiciona_usuario(username, password, email,
                                 first_name, is_superuser)

    return HttpResponse(json.dumps(user_dict), content_type='application/json')


def adiciona_usuario(username, password, email, first_name, is_superuser):
    user_dict = None

    if username and password and email and first_name:

        try:
            user_exist = User.objects.get(username=username)
        except:
            user_exist = None

        if user_exist is None:
            user = User.objects.create_user(username, password, email)

            user.first_name = first_name
            user.set_password(password)
            user.is_superuser = is_superuser
            user.save()
            user_dict = _user2dict(user)

    return user_dict


def logout(request):
    auth.logout(request)
    return HttpResponse('{}', content_type='application/json')


def _whoami(request):
    if request.user.is_authenticated():
        i_am = {
            'user': _user2dict(request.user),
            'authenticated': True,
        }
    else:
        i_am = {'authenticated': False}

    return i_am


def whoami(request):
    i_am = _whoami(request)
    return HttpResponse(json.dumps(i_am), content_type='application/json')


def get_user_details(request):
    username = request.GET['username']
    user = auth.get_user_model().objects.get(username=username)
    user_dict = _user2dict(user)
    return HttpResponse(json.dumps(user_dict), content_type='application/json')


@ajax_login_required
def list_topicos(request):
    filters = json.loads(request.GET.get('filters', '{}'))
    topicos_dic = pega_topicos()

    return HttpResponse(json.dumps(topicos_dic), content_type='application/json')


def pega_topicos():
    topicos = Topico.objects.all()
    topicos_dic = [t.to_dict_json() for t in topicos]
    for t in topicos_dic:
        user = t['id_usuario']
        t['id_usuario'] = user.id

    return topicos_dic


@ajax_login_required
def edita_topico(request):
    topico_id = json.loads(request.GET.get('topico_id'))
    topico_editado = request.GET.get('topico_editado')
    i_am = _whoami(request)['user']

    resposta = update_topico(topico_id, topico_editado, i_am['username'])

    return HttpResponse(json.dumps(resposta), content_type='application/json')


def update_topico(topico_id, topico_editado, username):
    if topico_editado:
        try:
            topico_exists = Topico.objects.get(name=topico_editado)
            return 'Esse nome eh invaliado'
        except Topico.DoesNotExist:
            try:
                topico = Topico.objects.get(id=topico_id)
            except:
                return 'Topico Invalido'

            try:
                i_am = User.objects.get(username=username)
            except:
                return 'Usuario Invalido'

            user = topico.id_usuario

            if user.id == i_am.id or (i_am.is_superuser
               and user.is_superuser == False):

                try:
                    topico.name = topico_editado
                    topico.save()
                    return "Topico salvo com sucesso"
                except:
                    return "Topico nao pode ser salvo"
            else:
                return 'Voce nao pode modificar esse topico'
    else:
        return 'O nome do topico nao pode ficar em branco'


@ajax_login_required
def list_mensagens(request):
    topico_id = request.GET.get('topico_id')

    if topico_id is None:
        logger.error('Nenhum topico encontrado, retornando []')
        return HttpResponse('[]', content_type='application/json')

    topico_id = json.loads(topico_id)

    mensagens_dict = get_mensagens(topico_id)

    return HttpResponse(json.dumps(mensagens_dict), content_type='application/json')


def get_mensagens(topico_id):

    if topico_id:
        try:
            thread = Topico.objects.get(id=topico_id)
        except:
            return []

        try:
            todas_mensagens = Mensagem.objects.filter(id_topico=thread)
        except:
            return []

        mensagens_dict = [m.to_dict_json() for m in todas_mensagens]
        for m in mensagens_dict:
            user = m['id_usuario']
            m['usuario_nome'] = user.username
            m['data'] = str(m['data'])
            m['data'] = m['data'].split('+')[0]
            m['data'] = m['data'].split('.')[0]
            m['id_topico'] = ''
            m['id_usuario'] = user.id
    else:
        mensagens_dict = []

    return mensagens_dict


@ajax_login_required
def deleta_mensagem(request):
    usuario_id = request.GET.get('usuario_id')
    mensagem_id = request.GET.get('mensagem_id')

    if usuario_id and mensagem_id:
        usuario_id = json.loads(usuario_id)
        mensagem_id = json.loads(mensagem_id)

        i_am = _whoami(request)['user']

        mensagem_dict = deletar_mensagembd(usuario_id, mensagem_id, i_am['username'])

    return HttpResponse(json.dumps(mensagem_dict), content_type='application/json')


def deletar_mensagembd(usuario_id, mensagem_id, username):
    mensagem_dict = 'Mansagem nao encontrada'

    try:
        user = User.objects.get(id=usuario_id)
    except:
        return 'Usuario Invalido'

    try:
        i_am = User.objects.get(username=username)
    except:
        return 'Voce precisa logar para ter acesso a essa funcionalidade'

    if i_am.id == user.id:
        try:
            mensagem_dict = _deletar(mensagem_id)
        except:
            mensagem_dict = 'Mensagem nao existe'
    elif i_am.is_superuser and user.is_superuser == False:
        try:
            mensagem_dict = _deletar(mensagem_id)
        except:
            mensagem_dict = 'Mensagem nao existe'
    else:
        mensagem_dict = 'Mensagem nao pode ser deletada por você'

    return mensagem_dict


def _deletar(mensagem_id):
    try:
        mensagem = Mensagem.objects.filter(id=mensagem_id)
        mensagem.delete()
        return 'Mensagem deletada com sucesso'
    except:
        return 'Mensagem id invalido'


@ajax_login_required
def registra_mensagem(request):
    topico_id = json.loads(request.GET.get('topico_id'))
    mensagem = request.GET.get('mensagem')
    i_am = _whoami(request)['user']

    mensagem_dict = salva_mensagem(topico_id, mensagem, i_am['username'])

    return HttpResponse(json.dumps(mensagem_dict), content_type='application/json')


def salva_mensagem(topico_id, mensagem, username):

    try:
        usuario = User.objects.get(username=username)
    except:
        return 'Usuario Invalido'

    try:
        thread = Topico.objects.get(id=topico_id)
    except:
        return 'Topico Invalido'

    try:
        m = Mensagem(id_usuario=usuario, id_topico=thread, conteudo=mensagem)
        m.save()
        return "Mensagem salva com sucesso"
    except:
        return "Mensagem nao pode ser salva no momento"


@ajax_login_required
def registra_topico(request):
    topico = request.GET.get('topico')
    mensagem = request.GET.get('mensagem')
    i_am = _whoami(request)['user']

    mensagem_topico = salva_topico(topico, mensagem, i_am['username'])

    return HttpResponse(json.dumps(mensagem_topico), content_type='application/json')


def salva_topico(topico, mensagem, username):
    if topico and mensagem:
        try:
            usuario = User.objects.get(username=username)
        except:
            return 'Esse usuario nao existe'

        try:
            topico_existe = Topico.objects.get(name=topico)
            return 'Topico ja existe'
        except:
            thread = Topico(name=topico, id_usuario=usuario)
            thread.save()

            m = Mensagem(id_usuario=usuario, id_topico=thread, conteudo=mensagem)
            m.save()
            return 'Topico adicionado com sucesso'
    else:
        return 'Existem campos em branco'


@ajax_login_required
def deleta_topico(request):
    topico_id = topico = request.GET.get('topico_id')

    if topico_id:
        topico_id = json.loads(topico_id)
        i_am = _whoami(request)['user']

        mensagem_delete = deletar_topico(topico_id, i_am['username'])
    else:
        mensagem_delete = 'Topico nao existe'

    return HttpResponse(json.dumps(mensagem_delete), content_type='application/json')


def deletar_topico(topico_id, username):
    try:
        topico = Topico.objects.get(id=topico_id)
    except:
        return 'Topico invalido'

    try:
        i_am = User.objects.get(username=username)
    except:
        return 'Usuario Invalido'

    user = topico.id_usuario

    if i_am.id == user.id or (i_am.is_superuser and user.is_superuser == False):
        mensagens_deletadas = Mensagem.objects.filter(id_topico=topico.id)
        try:
            for m in mensagens_deletadas:
                Mensagem.objects.filter(id=m.id).delete()
            topico.delete()
            return 'Topico deletado com sucesso'
        except:
            return 'O topico nao pode ser deletado'
    else:
        return 'Topico nao pode ser deletada por você'


def _user2dict(user):
    return {
        'username': user.username,
        'name': user.first_name,
        'permissions':{
            'ADMIN': user.is_superuser,
            'STAFF': user.is_staff,
        }
    }
