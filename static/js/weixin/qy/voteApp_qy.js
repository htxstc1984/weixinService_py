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
        var checked = $('#btn' + item_id).hasClass('itemselected');
        if (checked) {
            $('#btn' + item_id).removeClass('itemselected');
            $('#btn' + item_id).addClass('itemnoselected');
            $('#btn' + item_id+' i').removeClass('fa-thumbs-up');
            $('#btn' + item_id+' i').addClass('fa-thumbs-o-up');
            //$('#btn' + item_id).html('<i class="fa fa-thumbs-o-up fa-lg pull-right"></i>')
            //$('#btn' + item_id).text('请选择')
        } else {
            $scope.selectItems.push(item_id);
            $('#btn' + item_id).removeClass('itemnoselected');
            $('#btn' + item_id).addClass('itemselected');
            $('#btn' + item_id+' i').removeClass('fa-thumbs-o-up');
            $('#btn' + item_id+' i').addClass('fa-thumbs-up');
            //$('#btn' + item_id).empty()
            //$('#btn' + item_id).html('<i class="fa fa-thumbs-up fa-lg pull-right"></i>')
            //$('#btn' + item_id).text('已选')
        }
        //alert($scope.selectItems.length)
    }

    $scope.submit = function () {
        $scope.selectItems = new Array();
        $('.itemselected').each(function () {
            $scope.selectItems.push($(this).attr('bindid'));
        })
        $('#submitModal').modal({
            keyboard: true
        })
    }

    $scope.submitMsg = "";
    $scope.submitAction = function () {
        bz = $('#bz').val();
        $http.post('/mobi/vote/qy/submit', {
            schema_id: schema_id,
            bz: bz,
            selectItems: $scope.selectItems
        }).success(function (data) {
            if (data == 'error') {
                $scope.submitMsg = '提交失败，请刷新页面重试';
            } else {
                $scope.submitMsg = '投票成功';
                location.reload()
            }
            $('#msgModal').modal({
                keyboard: true
            })
        })
    }

    $scope.fullSelect = function () {
        $scope.selectItems = new Array();
        $('.itemselected').each(function () {
            $scope.selectItems.push($(this).attr('bindid'));
        })
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