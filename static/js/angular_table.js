var app = angular.module("app", ["xeditable", "ngMockE2E"]);
app.run(function(editableOptions) {
  editableOptions.theme = 'bs3';
});
// 获取涨停被砸股票

app.controller('CtrlOne', function($scope, $filter, $q, $http) {
    $scope.today = new  Date();
    $scope.timeString = $filter('date')($scope.today, 'yyyy-MM-dd');
    $scope.count = 0;
    $scope.users = [
        {id: 1, code: 300019, name: '硅宝科技', time: '19:30', frequency: 4, concept:'', isDeleted: false},
    ];

    $scope.showTime = function(user) {
        if(user.time) {
      return user.time.replace('red', '').replace('bold', '');
    } else {
      return 'Not set';
    }
    };
    $scope.showName = function(user) {
        $scope.count = $scope.count + 1
        var isName = false
        if(user.name)
          isName = true
        return isName ? user.name.replace('red', '').replace('bold', '') : 'Not set';
    };
    $scope.showFrequency = function(user) {
        if(user.frequency) {
      return user.frequency.toString().replace('red', '').replace('bold', '');
    } else {
      return 'Not set';
    }
    };
    $scope.showConcept = function(user) {
        if(user.concept) {
      return user.concept.replace('red', '').replace('bold', '');
    } else {
      return 'Not set';
    }
    };
    $scope.checkName = function(data, id) {
        if (data == '') {
      return "股票名称不能为空";
    }
    };
    // filter users to show
    $scope.filterUser = function(user) {
        return user.isDeleted !== true;
    };
    // mark user as deleted
    $scope.deleteUser = function(id) {
        var filtered = $filter('filter')($scope.users, {id: id});
        if (filtered.length) {
          filtered[0].isDeleted = true;
        }
    };
    // add user
    $scope.generateInfo = function() {
        var settings = {
          "async": true,
          "crossDomain": true,
          "url": "http://123.57.81.203:5000/getTodayCodeInfo?code="+$scope.TableCode ,
          "method": "GET",
          "data": ""
     }
        $.ajax(settings).done(function (response) {
            responseJson = eval('(' + response + ')');
            responseJson['id'] = $scope.users.length + 1;
            $scope.users.push(responseJson);
        });
    };
    // cancel all changes
    $scope.cancel = function() {
    for (var i = $scope.users.length; i--;) {
      var user = $scope.users[i];
      if (user.isDeleted) {
        delete user.isDeleted;
      }
      // remove new
      if (user.isNew) {
        $scope.users.splice(i, 1);
      }
    };
    };
    // save edits
    $scope.saveTable = function() {
    var results = [];
    for (var i = $scope.users.length; i--;) {
      var user = $scope.users[i];
      // actually delete user
      if (user.isDeleted) {
        $scope.users.splice(i, 1);
      }
      // mark as not new
      if (user.isNew) {
        user.isNew = false;
      }
      // send on server
      results.push($http.post('/saveUser', user));
    }
    return $q.all(results);
    };
});
app.controller('CtrlRedian', function($scope, $filter, $q, $http) {
    $scope.today = new  Date();
    $scope.timeString = $filter('date')($scope.today, 'yyyy-MM-dd');
    $scope.count = 0;
    $scope.users = [
        {id: 1, code: 300019, name: '硅宝科技', time: '19:30', frequency: 4, concept:'', isDeleted: false},
    ];

    $scope.showTime = function(user) {
        if(user.time) {
          return user.time.replace('red', '').replace('bold', '');
        } else {
          return 'Not set';
        }
    };
    $scope.showName = function(user) {
        $scope.count = $scope.count + 1
        var isName = false
        if(user.name)
          isName = true
        return isName ? user.name.replace('red', '').replace('bold', '') : 'Not set';
    };
    $scope.showFrequency = function(user) {
        if(user.frequency) {
      return user.frequency.toString().replace('red', '').replace('bold', '');
    } else {
      return 'Not set';
    }
    };
    $scope.showConcept = function(user) {
        if(user.concept) {
      return user.concept.replace('red', '').replace('bold', '');
    } else {
      return 'Not set';
    }
    };
    $scope.checkName = function(data, id) {
        if (data == '') {
      return "股票名称不能为空";
    }
    };
    // filter users to show
    $scope.filterUser = function(user) {
        return user.isDeleted !== true;
    };
    // mark user as deleted
    $scope.deleteUser = function(id) {
        var filtered = $filter('filter')($scope.users, {id: id});
        if (filtered.length) {
          filtered[0].isDeleted = true;
        }
    };
    // add user
    $scope.generateInfo = function() {
        var settings = {
          "async": true,
          "crossDomain": true,
          "url": "http://123.57.81.203:5000/getTodayCodeInfo?code="+$scope.TableCode ,
          "method": "GET",
          "data": ""
     }
        $.ajax(settings).done(function (response) {
            responseJson = eval('(' + response + ')');
            responseJson['id'] = $scope.users.length + 1;
            $scope.users.push(responseJson);
        });
    };
    // cancel all changes
    $scope.cancel = function() {
    for (var i = $scope.users.length; i--;) {
      var user = $scope.users[i];
      if (user.isDeleted) {
        delete user.isDeleted;
      }
      // remove new
      if (user.isNew) {
        $scope.users.splice(i, 1);
      }
    };
    };
    // save edits
    $scope.saveTable = function() {
    var results = [];
    for (var i = $scope.users.length; i--;) {
      var user = $scope.users[i];
      // actually delete user
      if (user.isDeleted) {
        $scope.users.splice(i, 1);
      }
      // mark as not new
      if (user.isNew) {
        user.isNew = false;
      }
      // send on server
      results.push($http.post('/saveUser', user));
    }
    return $q.all(results);
    };
});
app.controller('CtrlOther', function($scope, $filter, $q, $http) {
    $scope.today = new  Date();
    $scope.timeString = $filter('date')($scope.today, 'yyyy-MM-dd');
    $scope.count = 0;
    $scope.users = [
        {id: 1, code: 300019, name: '硅宝科技', time: '19:30', frequency: 4, concept:'', isDeleted: false},
    ];

    $scope.showTime = function(user) {
        if(user.time) {
          return user.time.replace('red', '').replace('bold', '');
        } else {
          return 'Not set';
        }
    };
    $scope.showName = function(user) {
        $scope.count = $scope.count + 1
        var isName = false
        if(user.name)
          isName = true
        return isName ? user.name.replace('red', '').replace('bold', '') : 'Not set';
    };
    $scope.showFrequency = function(user) {
        if(user.frequency) {
      return user.frequency.toString().replace('red', '').replace('bold', '');
    } else {
      return 'Not set';
    }
    };
    $scope.showConcept = function(user) {
        if(user.concept) {
      return user.concept.replace('red', '').replace('bold', '');
    } else {
      return 'Not set';
    }
    };
    $scope.checkName = function(data, id) {
        if (data == '') {
      return "股票名称不能为空";
    }
    };
    // filter users to show
    $scope.filterUser = function(user) {
        return user.isDeleted !== true;
    };
    // mark user as deleted
    $scope.deleteUser = function(id) {
        var filtered = $filter('filter')($scope.users, {id: id});
        if (filtered.length) {
          filtered[0].isDeleted = true;
        }
    };
    // add user
    $scope.generateInfo = function() {
        var settings = {
          "async": true,
          "crossDomain": true,
          "url": "http://123.57.81.203:5000/getTodayCodeInfo?code="+$scope.TableCode ,
          "method": "GET",
          "data": ""
     }
        $.ajax(settings).done(function (response) {
            responseJson = eval('(' + response + ')');
            responseJson['id'] = $scope.users.length + 1;
            $scope.users.push(responseJson);
        });
    };
    // cancel all changes
    $scope.cancel = function() {
    for (var i = $scope.users.length; i--;) {
      var user = $scope.users[i];
      if (user.isDeleted) {
        delete user.isDeleted;
      }
      // remove new
      if (user.isNew) {
        $scope.users.splice(i, 1);
      }
    };
    };
    // save edits
    $scope.saveTable = function() {
    var results = [];
    for (var i = $scope.users.length; i--;) {
      var user = $scope.users[i];
      // actually delete user
      if (user.isDeleted) {
        $scope.users.splice(i, 1);
      }
      // mark as not new
      if (user.isNew) {
        user.isNew = false;
      }
      // send on server
      results.push($http.post('/saveUser', user));
    }
    return $q.all(results);
    };
});
app.controller('CtrlZtbz', function($scope, $filter, $q, $http) {
    console.log(ztbz_num);
    $scope.today = new  Date();
    $scope.timeString = $filter('date')($scope.today, 'yyyy-MM-dd');
    $scope.title = "涨停被砸股票池 (" + ztbz_num + ")";
    $scope.count = 0;
    $scope.users = JSON.parse(ztbz_list);
    $scope.showChg = function(user) {
        if(user.chg) {
          return user.chg.replace('red', '').replace('bold', '');
        } else {
          return 'Not set';
        }
    };
    $scope.showName = function(user) {
        $scope.count = $scope.count + 1
        var isName = false
        if(user.name)
          isName = true
        return isName ? user.name.replace('red', '').replace('bold', '') : 'Not set';
    };
    $scope.showConcept = function(user) {
        if(user.concept) {
          return user.concept.replace('red', '').replace('bold', '');
        } else {
          return 'Not set';
        }
    };
    $scope.checkName = function(data, id) {
        if (data == '') {
            return "股票名称不能为空";
        }
    };
    // filter users to show
    $scope.filterUser = function(user){
        return user.isDeleted !== true;
    };
    // mark user as deleted
    $scope.deleteUser = function(id) {
        var filtered = $filter('filter')($scope.users, {id: id});
        if (filtered.length) {
          filtered[0].isDeleted = true;
        }
    };
    // add user
    $scope.generateInfo = function() {
        var settings = {
          "async": true,
          "crossDomain": true,
          "url": "http://123.57.81.203:5000/getTodayCodeInfo?code="+$scope.TableCode ,
          "method": "GET",
          "data": ""
        }
        $.ajax(settings).done(function (response) {
            responseJson = eval('(' + response + ')');
            responseJson['id'] = $scope.users.length + 1;
            $scope.users.push(responseJson);
        });
    };
    // cancel all changes
    $scope.cancel = function() {
    for (var i = $scope.users.length; i--;) {
      var user = $scope.users[i];
      if (user.isDeleted) {
        delete user.isDeleted;
      }
      // remove new
      if (user.isNew) {
        $scope.users.splice(i, 1);
      }
    };
    };
    // save edits
    $scope.saveTable = function() {
        var results = [];
        for (var i = $scope.users.length; i--;) {
          var user = $scope.users[i];
          // actually delete user
          if (user.isDeleted) {
            $scope.users.splice(i, 1);
          }
          // mark as not new
          if (user.isNew) {
            user.isNew = false;
          }
          // send on server
          results.push($http.post('/saveUser', user));
        }
        return $q.all(results);
    };
});
app.controller('UploadController', function($scope, $filter, $q, $http) {

});
 //------------ mock $http requests ---------------------
app.run(function($httpBackend) {
  $httpBackend.whenGET('/groups').respond([
    {id: 1, text: 'user'},
    {id: 2, text: 'customer'}
  ]);

  $httpBackend.whenPOST(/\/saveUser/).respond(function(method, url, data) {
    data = angular.fromJson(data);
    return [200, {status: 'ok'}];
  });
});