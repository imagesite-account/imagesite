var app = angular.module('viewApp', []);
// .service('albumInfo', function ($http) {
//     $scope.api_url = global_current_host + '/album/api/' + album_id;
//     $scope.all = 0;
//     var promise = $http.get($scope.api_url).
//     success(function (response) {
//       $scope.all = response.data;
//       $scope.images = $scope.all['image_list'];
//       $scope.labels = $scope.all['labels'];
//     });
//     return promise;
// });

// Required for csrf
// http://stackoverflow.com/questions/18156452/django-csrf-token-angularjs
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('viewController', function($scope, $http) {
  $scope.api_url = global_current_host + '/album/api/0/' + album_id;
  $scope.all = 0;
  $scope.images = ['http://i.imgur.com/kpXKVoo.png'];
  $scope.labels = [];
  $http({
      url: $scope.api_url,
      method: 'GET',
  }).
  then(function(response) {
      $scope.all = response.data;
      $scope.images = $scope.all['image_list'];
      $scope.labels = $scope.all['labels'];
  });

  $scope.initImg = function () {
    // return 'https://i.imgur.com/2B2JLbpm.jpg';
    return $scope.images[0];
  };
  $scope.viewImg = $scope.initImg();
  image_counter = 0;
  $scope.nextImg = function () {
    $scope.viewImg = 'https://i.imgur.com/uWc0eACm.jpg';
    image_counter++;
    $scope.viewImg = $scope.images[image_counter];
  };

});
