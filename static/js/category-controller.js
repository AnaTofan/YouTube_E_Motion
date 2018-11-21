angular.module('homeApp')
    .controller('categoryController', ['$scope', '$http', 'SERVER','$stateParams', function($scope, $http, server, $stateParams){
        $scope.test = 'test'
        $http.get(server + '/categories/' + $stateParams.id)
            .then((response) => {
                $scope.category = response.data.collection
                $scope.name = response.data.name
            })
            .catch((error) => console.warn(error))
    }])