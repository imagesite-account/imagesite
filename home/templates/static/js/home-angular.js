var app = angular.module('homeApp', []);

app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.controller('homeController', function($scope, $http) {
	  $scope.albums = [];
    $scope.api_albums_url = global_current_host + '/album/api/2/';

    $http({
        url: $scope.api_albums_url,
        method: 'GET',
    }).
    then(function(response) {
        var raw_data = response.data;
        for (i = 0; i < raw_data.length; i++){
            k = Math.floor(i / nxm_format);
            // alert(JSON.stringify(raw_data[i]));
            if (i % nxm_format == 0){
                $scope.albums.push([]);
            }
            raw_data[i]['link'] = '/album/' + raw_data[i]['album_id'];
            $scope.albums[k].push(raw_data[i]);
        }
        // alert(JSON.stringify($scope.albums));
//             album_list_ = []
// #     #     for i, album in enumerate(album_list):
// #     #         k = i // nxm_format
// #     #         if i % nxm_format == 0:
// #     #             album_list_.append([])
// #     #         album_list_[k].append(album)
// #     #         print('[view/api.py/get_all_album]: Album', album)
    });



});
