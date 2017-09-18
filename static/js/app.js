var app = angular.module("app",[]);

function getContent($scope,$http){
  var topstories=[];
  var stories=[];
  //get top stories
  $http.get('/topstories.json').then(function(response) {
    topstories=response.data;
      
    //get stories
    for(var i=0; i<10 ; i++){
      $http.get('/item/'+topstories[i]+'.json').then(function(response) {
          stories.push(response.data)
      });
    }
    $scope.stories=stories;
  });
}

app.controller('AppCtrl', function($scope,$http,$interval) {
  //disable En button by default   
  //show En content by default 
  $scope.disableEnButton=true;  
  $scope.viewContent='views/contentEn.html';

  //get content for the first time
  //update content every 10 minutes (600000 milliseconds)
  getContent($scope,$http);  
  $interval(function(){getContent($scope,$http)}, 600000 );
  
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
