(function(){

    var deps = [
        'component_catalog',
        'ui.router',
    ];
    if(window.DOCS && DOCS.angular_dependencies){
        deps = deps.concat(DOCS.angular_dependencies);
    }

    angular.module('docs_main', deps);
    angular.module('docs_main').config(function($interpolateProvider, $controllerProvider, $stateProvider, $urlRouterProvider) {
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}');

        $controllerProvider.allowGlobals();
        $urlRouterProvider.otherwise('/instructions');

        $stateProvider
            .state('base', {
                url: '/:category/:title',
                template: '<component-catalog-sample></component-catalog-sample>',
                controller: 'IncludeComponentCatalogSampleCtrl'
            })
            .state('instructions', {
                url: '/instructions',
                template: '<div layout-padding> select something on the left </div>'
            });
    });
})();

angular.module('component_catalog', ['ng_bind_html_unsafe']);
angular.module('component_catalog').factory('ComponentCatalog', function(){
    var catalog = {
        components: []
    };

    catalog.add_test_page = function(options){

        var component = {
            group: options.group,
            title: options.title,
            category: options.category,
            folder: options.folder,
            example: options.example,
            src: options.src,
            source_files: [],
        };
        catalog.components.push(component);
    };

    catalog.get = function(category, title){
        for(var i=0; i<catalog.components.length; i++){
            var component = catalog.components[i];
            if(component.category == category && component.title == title){
                return component;
            }
        }
    };

    function _2array(v){
        return !Array.isArray(v) && v !== undefined ? [v] : v;
    }

    return catalog;
});

angular.module('component_catalog').factory('ComponentCatalogViewModel', function(ComponentCatalog, $http, $templateCache){
    var m = {
        active_component: null,
        showing: 'NOTHING',
        components: [],
        categories: [],
        init: init,
        toggle_open: toggle_open,
        activate: activate,
        show_example: show_example,
        show_source: show_source,
        get_include: get_include,
        get_source: get_source,
    };

    function init(group_filter){
        m.components = ComponentCatalog.components.filter(function(e){
            return e.group == group_filter;
        });
        var catmap = {};
        m.categories = [];
        for(var i=0; i<m.components.length; i++){
            var category = m.components[i].category;
            if(!catmap[category]){
                m.categories.push({name: category});
                catmap[category] = true;
            }
        }
    }

    function toggle_open(category){
        category.open = !category.open;
    }

    function activate(component){

        function _loadfile(sourcefile){
            var url = DOCS.SAMPLE_BASE_URL + component.folder + sourcefile.name;
            $http.get(url).success(function(content){
                sourcefile.content = content;
            });
        }

        m.active_component = component;
        m.showing = 'EXAMPLE';
        if(component.source_files.length === 0){
            component.source_files = [{name: component.example}];
            if(component.src){
                component.source_files = component.source_files.concat(component.src.map(function(filename){ return {name: filename}; }));
            }
            component.source_files.map(_loadfile);
        }
        component.active_sourcefile = component.source_files[0];
    }

    function show_example(){
        m.showing = 'EXAMPLE';
    }

    function show_source(){
        m.showing = 'SOURCE';
    }

    function get_include(){
        return DOCS.SAMPLE_BASE_URL + m.active_component.folder + m.active_component.example;
    }

    function get_source(){
        return m.active_component.active_sourcefile.content;
    }

    return m;
});

angular.module('component_catalog').directive('componentCatalogTree', function(ComponentCatalogViewModel){
    return {
        restrict: 'E',
        scope: {
            group: '@'
        },
        templateUrl: DOCS.BASE_URL+'component_catalog/component_catalog_tree.html',
        controller: function($scope) {
            var m = $scope.m = ComponentCatalogViewModel;
            m.init($scope.group);

            $scope.by_category = function(category_name){
                return function(component){
                    return component.category == category_name;
                };
            };
        }
    };
});

angular.module('component_catalog').directive('componentCatalogSample', function(ComponentCatalogViewModel){
    return {
        restrict: 'E',
        scope: {},
        templateUrl: DOCS.BASE_URL+'component_catalog/sample_page.html',
        controller: function($scope) {
            var m = $scope.m = ComponentCatalogViewModel;
        }
    };
});

angular.module('component_catalog').controller('IncludeComponentCatalogSampleCtrl', function($scope, $stateParams, ComponentCatalog, ComponentCatalogViewModel){
    var category = $stateParams.category;
    var title = $stateParams.title;
    var component = ComponentCatalog.get(category, title);
    ComponentCatalogViewModel.activate(component);
});

angular.module("docstemplates", []).run(["$templateCache", function($templateCache) {$templateCache.put("TEMPLATE_CACHE/component_catalog/component_catalog_tree.html","<div><ul class=\"nav nav-sidebar\" ng-repeat=\"category in m.categories | orderBy: \'name\' \"><li class=\"group\"><a href ng-click=\"m.toggle_open(category)\"><span class=\"glyphicon glyphicon-plus\" ng-hide=\"category.open\"></span> <span class=\"glyphicon glyphicon-minus\" ng-show=\"category.open\"></span> <span>{[{category.name}]}</span></a></li><li ng-show=\"category.open\" ng-class=\"{active: component == m.active_component}\" ng-repeat=\"component in m.components | filter: by_category(category.name) | orderBy: \'name\'\"><a href=\"#/{[{component.category}]}/{[{component.title}]}\">{[{component.title}]}</a></li></ul></div>");
$templateCache.put("TEMPLATE_CACHE/component_catalog/sample_page.html","<div><div class=\"btn-group\" role=\"group\"><h1>{[{m.active_component.title}]}</h1><button class=\"btn btn-success\" ng-class=\"{\'active\': m.showing == \'EXAMPLE\'}\" ng-click=\"m.show_example()\">Example</button> <button class=\"btn btn-success\" ng-class=\"{\'active\': m.showing == \'SOURCE\'}\" ng-click=\"m.show_source()\">View Source</button></div><div style=\"margin-top: 20px\"><div ng-if=\"m.showing == \'EXAMPLE\'\" ng-include=\"m.get_include()\"></div><div ng-if=\"m.showing == \'SOURCE\'\"><ul><li ng-repeat=\"sourcefile in m.active_component.source_files\">{[{sourcefile.name}]}<pre>{[{sourcefile.content}]}</pre></li></ul></div></div></div>");}]);