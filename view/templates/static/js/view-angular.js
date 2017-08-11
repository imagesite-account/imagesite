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
  $scope.images = ['http://i.imgur.com/DLv7QiM.png'];
  $scope.labels = [];
  $scope.messages = {
    default: 'Input a rating for this image.',
    norating: 'You cannot submit until you have input a rating.',
    serverfault: 'No response from server.',
    end: 'There are no more images to rate.',
    custom: '',
  }

  $scope.disp_message = $scope.messages.default;
  $scope.image = {rating: false};

  // $scope.interim_response = {'init': 'init'};
  $http({
      url: $scope.api_image_url,
      method: 'GET',
  }).
  then(function(response) {
      $scope.all = response.data;
      $scope.images = $scope.all['image_list'];
      for (var i = 0; i < $scope.all['labels'].length; i++){
        $scope.labels.push({name: $scope.all['labels'][i]});
      }
      // $scope.labels = $scope.all['labels'];
      // alert('Inside api call:' + $scope.images);
      $scope.viewImg = $scope.initImg();
      // alert($scope.images);
  });
  // alert('Outside api call:' + $scope.images);
  image_counter = 0;
  $scope.initImg = function () {
    // return 'https://i.imgur.com/2B2JLbpm.jpg';
    // alert('Inside initImg:' + $scope.images);
    image_counter++;
    return $scope.images[0];
  };
  // $scope.viewImg = $scope.initImg();

  $scope.nextImg = function (rating) {
    // $scope.viewImg = 'https://i.imgur.com/uWc0eACm.jpg';
    // image_counter++;
    // alert(image_counter);
    // alert(JSON.stringify({'rating': rating, 'image_id': $scope.images[image_counter], image_counter}));
    var interim_submission = {'rating': rating, 'image_id': $scope.images[image_counter-1], }


    if (image_counter < $scope.images.length){
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
          }else{
            // alert(JSON.stringify($scope.interim_response['messages']));
            $scope.messages.custom = $scope.interim_response['messages']['additional_message'];
            $scope.disp_message = $scope.messages.custom;
          }
      });
      // $scope.interim_response = JSON.parse(JSON.stringify($scope.interim_response));
      // alert(JSON.stringify($scope.interim_response));
      $scope.viewImg = $scope.images[image_counter];
      $scope.disp_message = $scope.messages.default;
    }else if (image_counter === $scope.images.length){
      // alert('Last Image ' + image_counter + ' ' + $scope.images.length);
      $scope.viewImg = endscreen_link;
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
          }else{
            // alert('Unsuccessful in submitting rating');
            $scope.messages.custom = $scope.interim_response['messages']['additional_message'];
            $scope.disp_message = $scope.messages.custom;
          }
      });
      image_counter++;
      $scope.viewImg = endscreen_link;
      $scope.disp_message = $scope.messages.end;
    }else{
      image_counter++;
      $scope.viewImg = endscreen_link;
      $scope.disp_message = $scope.messages.end;
    }

  };

  $scope.submit = function (){
    // http://jsfiddle.net/mrajcok/7MhLd/
    // https://stackoverflow.com/questions/13714884/difficulty-with-ng-model-ng-repeat-and-inputs
    // $scope.image = {2:2};
    // alert(JSON.stringify($scope.image));

    if ($scope.image.rating === false){
      $scope.disp_message = $scope.messages.norating;
    }else{
      document.getElementById("button-submit").disabled = true;
      $scope.nextImg($scope.image.rating);
      document.getElementById("button-submit").disabled = false;

      $scope.image.rating = false;
    }


  };


});
