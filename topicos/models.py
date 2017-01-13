from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible

class Topico(models.Model):
    name = models.CharField(max_length=256)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def to_dict_json(self):
    	return {
            'id': self.id,
    		'name': self.name,
            'id_usuario':self.id_usuario
    	}


class Mensagem(models.Model):
    conteudo = models.CharField(max_length=256)
    data = models.DateTimeField(auto_now_add=True)
    id_topico = models.ForeignKey(Topico, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def to_dict_json(self):
    	return {
            'id': self.id,
    		'conteudo': self.conteudo,
            'data': self.data,
            'id_topico': self.id_topico,
            'id_usuario': self.id_usuario,
    	}
