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
        var checked = $('#btn' + item_id).hasClass('btn-danger');
        if (checked) {
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
        $scope.selectItems = new Array();
        $('.btn-danger').each(function () {
            $scope.selectItems.push($(this).attr('bindid'));
        })
        $('#submitModal').modal({
            keyboard: true
        })
    }

    $scope.submitMsg = "";
    $scope.submitAction = function () {
        $http.post('/mobi/vote/submit', {
            openid: openid,
            schema_id: schema_id,
            selectItems: $scope.selectItems
        }).success(function (data) {
            if (data == 'error') {
                $scope.submitMsg = '提交失败，请刷新页面重试';
            } else {
                $scope.submitMsg = '投票成功';
            }
            $('#msgModal').modal({
                keyboard: true
            })
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