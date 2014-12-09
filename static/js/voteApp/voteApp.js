/**
 * Created by hu on 2014/12/8.
 */
var app = angular.module('voteApp', []);
app.controller('appController', function ($scope, $http) {
    $scope.detailItem = {
        itemtitle: '',
        itemdesc: '',
        picurl: ''
    }

    $scope.selectItems = new Array();

    $scope.addSelect = function (item_id) {
        var _exist = $.inArray(item_id, $scope.selectItems);
        if (_exist != -1) {
            $scope.selectItems.pop(item_id);
            $('#btn' + item_id).removeClass('btn-danger');
            $('#btn' + item_id).addClass('btn-primary');
            $('#btn' + item_id).text('请选择')
        } else {
            $scope.selectItems.push(item_id);
            $('#btn' + item_id).removeClass('btn-primary');
            $('#btn' + item_id).addClass('btn-danger');
            $('#btn' + item_id).text('已选')
        }
        //alert($scope.selectItems.length)
    }

    $scope.submit = function () {
        $('#submitModal').modal({
            keyboard: true
        })
    }

    $scope.submitAction = function () {
        $http.post('/mobi/vote/submit', $scope.selectItems).success(function (data) {
            alert("data:" + data)
        })
    }

    $scope.fullSelect = function () {
        return !($scope.selectItems.length == mutimax);
    }

    $scope.setItem = function (itemtitle, itemdesc, picurl) {
        $scope.detailItem.itemtitle = itemtitle;
        $scope.detailItem.itemdesc = itemdesc;
        $scope.detailItem.picurl = picurl;

        $('#detailModal').modal({
            keyboard: true
        })
    }
})