function appController($scope) {
    $scope.user = {
        firstname: 'huangtx',
        lastname: 'tingxi'
    };
    $scope.fullname = function () {
        return $scope.user.firstname + '' + $scope.user.lastname;
    };
}