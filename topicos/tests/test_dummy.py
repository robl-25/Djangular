import json
from topicos.views import adiciona_usuario, salva_topico, pega_topicos
from topicos.views import deletar_topico, get_mensagens, deletar_mensagembd
from topicos.views import salva_mensagem, update_topico
from django.test import TestCase
from django.contrib import auth
from topicos.models import Topico
from topicos.models import Mensagem
from django.contrib.auth.models import User

class DummyTest(TestCase):
    def test_cadastrar(self):
        resposta = adiciona_usuario('teste3', 'teste3', 'teste@mailinator.com',
                                    'teste', False)
        self.assertNotEquals(resposta, None)

        resposta = adiciona_usuario('teste', 'teste', 'teste@mailinator.com',
                                    'teste', True)
        self.assertNotEquals(resposta, None)

        resposta = adiciona_usuario('teste3', 'teste3', 'teste', 'teste', False)
        self.assertEquals(resposta, None)


    def test_pega_topicos(self):
        resposta = pega_topicos()
        self.assertEquals(resposta, [])

        adiciona_usuario('teste3', 'teste3', 'teste@mailinator.com',
                                    'teste', False)
        user = User.objects.get(username='teste3')
        topico = Topico(name='Testando', id_usuario=user)

        resposta = pega_topicos()

        topicos = Topico.objects.all()
        topicos_dic = [t.to_dict_json() for t in topicos]
        self.assertEquals(resposta, topicos_dic)


    def test_salva_topico(self):
        adiciona_usuario('teste3', 'teste3', 'teste@mailinator.com',
                                    'teste', False)

        resposta = salva_topico('Testando', 'teste', 'teste3')
        previsto = 'Topico adicionado com sucesso'
        self.assertEquals(resposta, previsto)

        resposta = salva_topico('Teste', 'teste', 'teste')
        previsto = 'Esse usuario nao existe'
        self.assertEquals(resposta, previsto)

        resposta = salva_topico('','','teste3')
        previsto = 'Existem campos em branco'
        self.assertEquals(resposta, previsto)

        adiciona_usuario('teste3', 'teste3', 'teste@mailinator.com',
                                    'teste', False)

        salva_topico('Testando', 'teste', 'teste3')
        resposta = salva_topico('Testando', 'teste', 'teste3')
        previsto = 'Topico ja existe'
        self.assertEquals(resposta, previsto)


    def test_deletar_topico(self):
        adiciona_usuario('teste3', 'teste3', 'teste@mailinator.com',
                                    'teste', False)

        resposta = salva_topico('Testando', 'teste', 'teste3')
        topico = Topico.objects.get(name='Testando')
        resposta = deletar_topico(topico.id, 'teste3')
        previsto = 'Topico deletado com sucesso'
        self.assertEquals(resposta, previsto)

        resposta = deletar_topico(None, 'teste3')
        previsto = 'Topico invalido'
        self.assertEquals(resposta, previsto)

        resposta = salva_topico('Testando', 'teste', 'teste3')
        topico = Topico.objects.get(name='Testando')
        resposta = deletar_topico(topico.id, 'teste')
        previsto = 'Usuario Invalido'
        self.assertEquals(resposta, previsto)

        adiciona_usuario('teste', 'teste', 'teste@mailinator.com',
                                    'teste', False)

        topico = Topico.objects.get(name='Testando')
        resposta = deletar_topico(topico.id, 'teste')
        previsto = 'Topico nao pode ser deletada por você'
        self.assertEquals(resposta, previsto)

        adiciona_usuario('teste4', 'teste4', 'teste@mailinator.com',
                                    'teste', False)
        adiciona_usuario('teste5', 'teste5', 'teste@mailinator.com',
                                    'teste', True)

        resposta = salva_topico('Testando', 'teste', 'teste4')
        topico = Topico.objects.get(name='Testando')
        resposta = deletar_topico(topico.id, 'teste5')
        previsto = 'Topico deletado com sucesso'
        self.assertEquals(resposta, previsto)


    def test_get_mensagens(self):
        adiciona_usuario('teste', 'teste', 'teste@mailinator.com',
                         'teste', False)

        salva_topico('Teste', 'hahaha', 'teste')
        topico = Topico.objects.get(name='Teste')

        resposta = get_mensagens(topico.id)

        todas_mensagens = Mensagem.objects.filter(id_topico=topico)
        mensagens_dict = [m.to_dict_json() for m in todas_mensagens]
        for m in mensagens_dict:
            user = m['id_usuario']
            m['usuario_nome'] = user.username
            m['data'] = str(m['data'])
            m['data'] = m['data'].split('+')[0]
            m['data'] = m['data'].split('.')[0]
            m['id_topico'] = ''
            m['id_usuario'] = user.id

        self.assertEquals(resposta, mensagens_dict)

        resposta = get_mensagens('')
        previsto = []
        self.assertEquals(resposta, previsto)

        reposta = get_mensagens(1)
        previsto = []
        self.assertEquals(resposta,previsto)

        adiciona_usuario('teste', 'teste', 'teste@mailinator.com',
                         'teste', False)

        salva_topico('Teste', 'hahaha', 'teste')
        topico = Topico.objects.get(name='Teste')
        mensagem = Mensagem.objects.filter(id_topico=topico.id)
        mensagem.delete()

        resposta = get_mensagens(topico.id)
        previsto = []
        self.assertEquals(resposta, previsto)


    def test_salva_mensagem(self):
        adiciona_usuario('teste', 'teste', 'teste@mailinator.com',
                         'teste', False)
        user = User.objects.get(username='teste')
        salva_topico('Teste', 'hahaha', 'teste')
        topico = Topico.objects.get(name='Teste')
        resposta = salva_mensagem(topico.id, 'hehehehe', user.username)
        previsto = 'Mensagem salva com sucesso'
        self.assertEquals(resposta, previsto)

        user = User.objects.get(username='teste')
        resposta = salva_mensagem('', 'hehehehe', user.username)
        previsto = 'Topico Invalido'
        self.assertEquals(resposta, previsto)

        topico = Topico.objects.get(name='Teste')
        resposta = salva_mensagem(topico.id, 'hehehehe', '')
        previsto = 'Usuario Invalido'
        self.assertEquals(resposta, previsto)


    def test_deletar_mensagembd(self):
        adiciona_usuario('teste', 'teste', 'teste@mailinator.com',
                         'teste', False)

        salva_topico('Teste', 'hahaha', 'teste')
        user = User.objects.get(username='teste')
        topico = Topico.objects.get(name='Teste')
        mensagem = Mensagem(id_usuario=user, id_topico=topico,
                            conteudo='hahaha')
        mensagem.save()
        resposta = deletar_mensagembd(user.id, mensagem.id, user.username)
        previsto = 'Mensagem deletada com sucesso'
        self.assertEquals(resposta, previsto)

        topico = Topico.objects.get(name='Teste')
        mensagem = Mensagem(id_usuario=user, id_topico=topico,
                            conteudo='hahaha')
        mensagem.save()
        resposta = deletar_mensagembd('', mensagem.id, user.username)
        previsto = 'Usuario Invalido'
        self.assertEquals(resposta, previsto)

        adiciona_usuario('teste2', 'teste2', 'teste@mailinator.com',
                         'teste', False)

        user = User.objects.get(username='teste')
        topico = Topico.objects.get(name='Teste')
        resposta = deletar_mensagembd(user.id, mensagem.id, 'teste2')
        previsto = 'Mensagem nao pode ser deletada por você'
        self.assertEquals(resposta, previsto)

        adiciona_usuario('teste3', 'teste3', 'teste@mailinator.com',
                         'teste', True)

        user = User.objects.get(username='teste')
        topico = Topico.objects.get(name='Teste')
        resposta = deletar_mensagembd(user.id, mensagem.id, 'teste3')
        previsto = 'Mensagem deletada com sucesso'
        self.assertEquals(resposta, previsto)

        user = User.objects.get(username='teste')
        topico = Topico.objects.get(name='Teste')
        resposta = deletar_mensagembd(user.id, mensagem.id, '')
        previsto = 'Voce precisa logar para ter acesso a essa funcionalidade'
        self.assertEquals(resposta, previsto)

        user = User.objects.get(username='teste')
        topico = Topico.objects.get(name='Teste')
        resposta = deletar_mensagembd(user.id, '', 'teste3')
        previsto = 'Mensagem id invalido'
        self.assertEquals(resposta, previsto)


    def test_update_topico(self):
        adiciona_usuario('teste3', 'teste3', 'teste@mailinator.com',
                                    'teste', False)

        salva_topico('Testando', 'teste', 'teste3')
        topico = Topico.objects.get(name='Testando')
        resposta = update_topico(topico.id, 'Teste', 'teste3')
        previsto = 'Topico salvo com sucesso'
        self.assertEquals(resposta, previsto)

        resposta = update_topico('', 'Teste2', 'teste3')
        previsto = 'Topico Invalido'
        self.assertEquals(resposta, previsto)

        resposta = update_topico(topico.id, '', 'teste3')
        previsto = 'O nome do topico nao pode ficar em branco'
        self.assertEquals(resposta, previsto)

        resposta = update_topico(topico.id, 'Teste3', '')
        previsto = 'Usuario Invalido'
        self.assertEquals(resposta, previsto)

        adiciona_usuario('teste', 'teste', 'teste@mailinator.com',
                                    'teste', False)

        resposta = update_topico(topico.id, 'Teste3', 'teste')
        previsto = 'Voce nao pode modificar esse topico'
        self.assertEquals(resposta, previsto)

        adiciona_usuario('teste2', 'teste2', 'teste@mailinator.com',
                                    'teste', True)

        resposta = update_topico(topico.id, 'Teste3', 'teste2')
        previsto = 'Topico salvo com sucesso'
        self.assertEquals(resposta, previsto)
