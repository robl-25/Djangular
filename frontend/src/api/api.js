angular.module('appapi', ['appajax']);

angular.module('appapi').factory('AppApi', function(AppAjax){
	var api = {
		add: todo,
		login: login,
		logout: logout,
		whoami: whoami,
		list_topicos: list_topicos,
		get_user_details: get_user_details,
		cadastro: cadastro,
		list_mensagens: list_mensagens,
		registra_mensagem: registra_mensagem,
		deleta_mensagem: deleta_mensagem,
		registra_topico: registra_topico,
		deleta_topico: deleta_topico,
		edita_topico: edita_topico
	};

	function todo(){}

	function login(username, password){
		return AppAjax.post('/api/login', {username: username, password: password});
	}

	function cadastro(username, password, nome, email, tipo){
		is_superuser = (tipo == 'admin');

		return AppAjax.post('/api/cadastro', {
			username: username,
			password: password,
			first_name: nome,
			email: email,
			is_superuser: is_superuser
		});
	}

	function logout(){
		return AppAjax.get('/api/logout');
	}

	function whoami(){
		return AppAjax.get('/api/whoami');
	}

	function list_topicos(filters){
		return AppAjax.get('/api/list_topicos', {filters: angular.toJson(filters)});
	}

	function edita_topico(filters){
		return AppAjax.get('/api/edita_topico', {
			topico_id: angular.toJson(topico_id),
			topico_editado: topico_editado
		});
	}

	function list_mensagens(topico_id){
		return AppAjax.get('/api/list_mensagens', {topico_id: angular.toJson(topico_id)});
	}

	function registra_mensagem(topico_id, mensagem){
		return AppAjax.get('/api/registra_mensagem', {
			topico_id: angular.toJson(topico_id),
			mensagem: mensagem
		});
	}

	function deleta_mensagem(mensagem_id, usuario_id){
		return AppAjax.get('/api/deleta_mensagem', {
			mensagem_id: angular.toJson(mensagem_id),
			usuario_id: angular.toJson(usuario_id)
		});
	}

	function registra_topico(topico, mensagem){
		return AppAjax.get('/api/registra_topico', {
			topico: topico,
			mensagem: mensagem
		});
	}

	function deleta_topico(topico_id){
		return AppAjax.get('/api/deleta_topico', {
			topico_id: angular.toJson(topico_id)
		});
	}

	function get_user_details(username){
		return AppAjax.get('/api/get_user_details', {username: username});
	}

	return api;
});
