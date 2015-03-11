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
    $scope.items_ps = defaultItems_ps;

    $scope.addSelect = function (item_id) {
        var checked = $('#btn' + item_id).hasClass('itemselected');
        if (checked) {
            $('#btn' + item_id).removeClass('itemselected');
            $('#btn' + item_id).addClass('itemnoselected');
            $('#btn' + item_id+' i').removeClass('fa-thumbs-up');
            $('#btn' + item_id+' i').addClass('fa-thumbs-o-up');
            //$scope.items_ps[item_id] = $scope.items_ps[item_id]-1
            $('#btn' + item_id).empty()
            $('#btn' + item_id).html('<i class="fa fa-check-circle fa-lg pull-right"><font color="green" size="small">请选择</font></i>')
            //$('#btn' + item_id).text('请选择')
        } else {
            //$scope.selectItems.push(item_id);
            $('#btn' + item_id).removeClass('itemnoselected');
            $('#btn' + item_id).addClass('itemselected');
            $('#btn' + item_id+' i').removeClass('fa-thumbs-o-up');
            $('#btn' + item_id+' i').addClass('fa-thumbs-up');
            //$scope.items_ps[item_id] = $scope.items_ps[item_id]+1
            $('#btn' + item_id).empty()
            $('#btn' + item_id).html('<i class="fa fa-check fa-lg pull-right"><font color="red" size="small">我最喜爱</font> </i>')
            //$('#btn' + item_id).text('已选')
        }
        //alert($scope.selectItems.length)
    }

    $scope.submit = function () {

        $('#submitModal').modal({
            keyboard: true
        })
    }

    $scope.submitMsg = "";
    $scope.submitAction = function () {
        $scope.selectItems = new Array();
        $('.itemselected').each(function () {
            $scope.selectItems.push($(this).attr('bindid'));
        })
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
                //location.reload()
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
        if($scope.selectItems.length > mutimax){
            $scope.submitMsg = '对不起，可选节目为'+mutimax+'个，您当前已选择'+$scope.selectItems.length+'个，将无法提交';
            $('#msgModal').modal({
                keyboard: true
            })
        }
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

    $scope.goods_display = function (item_id) {
        goods = $scope.items_ps[item_id]
        if (goods > 50 && goods <= 100){
            return '50+'
        }else if(goods > 100 && goods <= 200){
            return '100+'
        }else if(goods > 200 && goods <= 300){
            return '200+'
        }else if(goods > 300){
            return '300+'
        }
        return goods
    }
})