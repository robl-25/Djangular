angular.module('topicos', ['appapi']);

angular.module('topicos').factory('topicosRepository', function(AppApi, AppAuth, $state){
	var m = {
		loading: false,
		topicos: [],
		enviar_topico: '',
		enviar_mensagem: '',
		id_topico_edit: -1,
		editavel: false,
		topico_editado: ''
	};

	angular.extend(m, {
		init: init,
		registrar: registrar,
		load_topicos: load_topicos,
		cancelar: cancelar,
		goto_mensagens: goto_mensagens,
		deletar: deletar,
		editar: editar,
		identifica: identifica,
		salvar_edicao: salvar_edicao,
	});

	function init(){
		console.log("Entrando no init :D");
		m.enviar_mensagem = '';
		m.enviar_topico = '';
		loading = false;
		m.topicos = [];
		m.load_topicos();
	}

	function load_topicos(){
		console.log("Pegando topicos");
		m.topicos = [];
		m.loading = true;
		AppApi.list_topicos().then(function(result){
			m.topicos = result.data;
		}).finally(function(){
			m.loading = false;
		});
	}

	function cancelar(){
		m.id_topico_edit = -1;
		m.editavel = false;
		m.load_topicos();
	}

	function registrar(){
		console.log("Enviar topico");
		console.log(m.enviar_topico);
		console.log(m.enviar_mensagem);
		AppApi.registra_topico(m.enviar_topico, m.enviar_mensagem).then(function(result){
			alert(result.data);
			m.enviar_topico = '';
			m.enviar_mensagem = '';
			m.load_topicos();
		});
	}

	function deletar(topico_id){
		console.log("Enviar topico");
		console.log(topico_id);
		AppApi.deleta_topico(topico_id).then(function(result){
			alert(result.data);
			m.enviar_topico = '';
			m.enviar_mensagem = '';
			m.load_topicos();
		});
	}

	function salvar_edicao(){
		console.log("Editando topico")
		console.log(m.id_topico_edit);
		console.log(m.topico_editado);
		topico_id = m.id_topico_edit;
		topico_editado = m.topico_editado;
		AppApi.edita_topico(topico_id, topico_editado).then(
		function(result){
			alert(result.data);
			m.cancelar();
		});
	}

	function editar(topico_id, topico_name){
		m.id_topico_edit = topico_id;
		m.editavel = true;
		m.topico_editado = topico_name;
		m.load_topicos();
	}

	function identifica(topico_id){
		console.log("Entrou no identifica :D");
		if(m.editavel){
			if(m.id_topico_edit == topico_id){
				return true;
			}
			return false;
		}
		return false;
	}

	function goto_mensagens(id, nome){
		console.log("Clicked with id: " + id);
		console.log("Clicked with name: " + nome);
		m.enviar_mensagem = '';
		m.enviar_topico = '';
		$state.go("mensagens", {id_topico: id, nome_topico: nome});
	}

	return m;
});

angular.module('topicos').controller('TopicosController', function($scope, AppAuth, topicosRepository){
	console.log("Entrando no controller :D");
	topicosRepository.init();
	$scope.m = topicosRepository;
});

angular.module('topicos').directive('topicos', function(topicosRepository){
	return {
		restrict: 'E',
		replace: true,
		templateUrl: APP.BASE_URL+'topicos/topicos.html',
		controller: function($scope, AppAuth, topicosRepository){
			console.log("Entrando no controller :D");
			$scope.auth = AppAuth;
			topicosRepository.init();
			$scope.m = topicosRepository;
		},
	};
});
