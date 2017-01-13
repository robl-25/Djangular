angular.module('mensagens', ['appapi']);

angular.module('mensagens').factory('mensagensRepository', function(AppApi, $stateParams, $state){
	var m = {
		loading: false,
		mensagens: [],
		id_topico: -1,
		nome_topico: '',
		enviar_mensagem: '',
		mensagem_deletar: [],
	};

	angular.extend(m, {
		load_mensagens: load_mensagens,
		init: init,
		registrar: registrar,
		deletar: deletar,
	});

	function load_mensagens(){
		m.loading = true
		console.log("In mensagens, about to load data");
		console.log("Current topico_id: " + m.id_topico);
		console.log("Current topico_name: " + m.nome_topico);
		AppApi.list_mensagens(m.id_topico).then(function(result){
			m.loading = false;
			m.mensagens = result.data;
		});
	}

	function init(){
		console.log($stateParams);
		m.id_topico = $stateParams.id_topico;
		m.nome_topico = $stateParams.nome_topico;
		console.log(m.nome_topico);
		m.load_mensagens();
	}

	function registrar(){
		console.log("Enviar mensagem");
		AppApi.registra_mensagem(m.id_topico, m.enviar_mensagem).then(function(){
			alert("Mensagem salva com sucesso");
			m.enviar_mensagem = '';
			m.load_mensagens();
		});
	}

	function deletar(deleta_id, usuario_id){
		console.log("Deletar mensagem");
		console.log(usuario_id)
		console.log(deleta_id)
		AppApi.deleta_mensagem(deleta_id, usuario_id).then(function(result){
			var deletar = result.data;
			alert(deletar);
			m.load_mensagens();
		});
	}

	return m;
});

angular.module('mensagens').controller('MensagensController', function($scope, mensagensRepository){
	mensagensRepository.init();
	$scope.m = mensagensRepository;
});

angular.module('mensagens').directive('mensagens', function(mensagensRepository){
	return {
		restrict: 'E',
		replace: true,
		templateUrl: APP.BASE_URL+'mensagens/mensagens.html'
	};
});
