var app = angular.module('viewApp', []);

// Required for csrf
// http://stackoverflow.com/questions/18156452/django-csrf-token-angularjs
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('viewController', function($scope, $http) {
  $scope.initImg = function () {

    return 'https://i.imgur.com/2B2JLbpm.jpg'
  };
  $scope.viewImg = $scope.initImg();
  $scope.nextImg = function () {
    $scope.viewImg = 'https://i.imgur.com/uWc0eACm.jpg';
  };

});
