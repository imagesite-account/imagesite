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
  // Must append slash when submtting POST request to API
  $scope.api_image_url = global_current_host + '/album/api/0/' + album_id + '/';
  $scope.api_submit_url = global_current_host + '/album/api/1/' + album_id + '/';
  $scope.all = 0;
  $scope.images = ['http://i.imgur.com/kpXKVoo.png'];
  $scope.labels = [];

  // $scope.interim_response = {'init': 'init'};
  $http({
      url: $scope.api_image_url,
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
    // $scope.viewImg = 'https://i.imgur.com/uWc0eACm.jpg';
    // image_counter++;
    // alert(image_counter);
    var interim_submission = {'rating': 5, 'image_id': $scope.images[image_counter], }
    if (image_counter < $scope.images.length - 1){
      $http({
          url: $scope.api_submit_url,
          method: 'POST',
          data: interim_submission,
          // data: '000000',
          headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      }).
      then(function(response) {
          $scope.interim_response = response.data;
          // alert(JSON.stringify($scope.interim_response['messages']));
          // alert(10);
          if ($scope.interim_response['messages']['success'] === true){
            // alert('success');
            image_counter++;
          }
      });
      // $scope.interim_response = JSON.parse(JSON.stringify($scope.interim_response));
      // alert(JSON.stringify($scope.interim_response));


      $scope.viewImg = $scope.images[image_counter];
    }else{
      $scope.viewImg = endscreen_link;
    }

  };

});
