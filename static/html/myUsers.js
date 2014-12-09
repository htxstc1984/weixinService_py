function appController($scope) {
    $scope.itemDetail = {
        title: '',
        desc: '',
        picurl:''
    };
    $scope.fullname = function () {
        return $scope.user.firstname + '' + $scope.user.lastname;
    };
}