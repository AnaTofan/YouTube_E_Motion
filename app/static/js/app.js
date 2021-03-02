angular.module('homeApp', ['ui.router'])
    .config(['$urlRouterProvider', '$stateProvider', function($urlRouterProvider, $stateProvider){
        $urlRouterProvider.otherwise('/home')
        $stateProvider
            .state('about', {
                url : '/about',
                templateUrl : 'static/templates/about.html'
            })
            .state('home', {
                url : '/home',
                templateUrl : '/static/templates/home.html'
            })
            .state('details', {
                url : '/details/:id',
                templateUrl: '/static/templates/category.html'
            })
    }])
    .constant('SERVER','localhost:5000')

