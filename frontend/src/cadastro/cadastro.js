angular.module('appcadastro', ['appapi']);

angular.module('appcadastro').factory('AppCadastroModel', function(AppAuth, AppApi, $state){
	var m = {
		username: '',
		password: '',
		email: '',
		nome: '',
        tipo: '',
		cadastro: cadastro
	};

    function cadastro(){
		AppApi.cadastro(m.username, m.password, m.nome, m.email, m.tipo).then(
			function(result){
				var cadastrado_user = result.data


				if(cadastrado_user){
					alert("Cadastro realizado com sucesso");
					m.username = '';
					m.password = '';
					m.email = '';
					m.nome = '';
			        m.tipo = '';
					$state.go('login');

				} else {
					alert('Cadastro inválido! Verifique se não existem campos vazios, caso não exista o nome de usuário é inválido');
				}

		});
	}

	return m;
});

angular.module('appcadastro').directive('appcadastro', function(){
	return {
		restrict: 'E',
		replace: true,
		scope: {},
		templateUrl: APP.BASE_URL+'cadastro/cadastro.html',
        controller: function($scope, AppCadastroModel){
			$scope.m = AppCadastroModel;
		},
	};
});
