'use strict'
const server='127.0.0.1'
angular.module('homeApp')
    .controller('homeController', ['$scope', '$http' ,function($scope, $http){
        $http.get('/categories')
            .then((response) => {
                $scope.categories = response.data

            })
            .catch((error) => console.warn(error))
    }])