var app = angular.module("app",[]);

function getContent($scope,$http){
  var topstories=[];
  var stories=[];
  //get top stories
  $http.get('/topstories.json').then(function(response) {
    topstories=response.data;

    //get stories
    for(var i=0; i<topstories.length; i++){
      $http.get('/item/'+topstories[i]+'.json').then(function(response) {
          stories.push(response.data);
      });
    }
    $scope.stories=stories;
  });
}

function getTranslation($scope,$http,language){
  var trasn_key = 'trans_'+language;
  var trasn_data = [];
  $scope[trasn_key]=[];

  for(var i=0; i<$scope.stories.length; i++){
    id=$scope.stories[i].id
    //get translation data from stories id
    $http.get('/translation/'+id+'_'+language+'/').then(function(response) {
      trasn_data.push(response.data);
    });
  }
  $scope[trasn_key]=trasn_data;
}

function init($scope,$http){  

  var topstories=[];
  var stories=[];
  var trans_pt=[];
  var trans_es=[];
  //get top stories
  $http.get('/topstories.json').then(function(response) {
    topstories=response.data;

    //get stories
    for(var i=0; i<topstories.length; i++){
      var id = topstories[i];
      $http.get('/item/'+id+'.json').then(function(response) {
        stories.push(response.data);
      });
      $http.get('/translation/'+id+'_pt/').then(function(response) {
        trans_pt.push(response.data);
      });
      $http.get('/translation/'+id+'_es/').then(function(response) {
        trans_es.push(response.data);
      });

    }
    $scope.stories=stories;
    $scope.trans_pt=trans_pt;
    $scope.trans_es=trans_es;
  });
}

app.controller('AppCtrl', function($scope,$http,$interval) {
  
  //disable En button by default   
  //show En content by default 
  $scope.disableEnButton=true;  
  $scope.viewContent='views/contentEn.html';
  $scope.dashboard='views/dashboard.html'
  init($scope,$http);

  $scope.refreshContent = function(){    
    return init($scope,$http);
  }
  
  //change content view and disable language button
  $scope.changeTopLang = function(lang){
    $scope.disableEnButton=false;
    $scope.disablePtButton=false;
    $scope.disableEsButton=false;
    
    switch (lang) {
      case 0:
        $scope.disableEnButton=true;
        $scope.viewContent='views/contentEn.html';
        break;
      case 1:
        $scope.disablePtButton=true;
        $scope.viewContent='views/contentPt.html';
        break;
      case 2:
        $scope.disableEsButton=true;
        $scope.viewContent='views/contentEs.html';
        break;
    }
  }
});
