angular.module('sortApp', [])

.controller('mainController', function($scope) {
  $scope.sortType     = 'name'; // set the default sort type
  $scope.sortReverse  = false;  // set the default sort order
  $scope.searchItem   = '';     // set the default search/filter term

  // create the list of sushi rolls
  $scope.sushi = [
    { name: 'Cali Roll', item: 'Crab', tastiness: 2 },
    { name: 'Philly', item: 'Tuna', tastiness: 4 },
    { name: 'Tiger', item: 'Eel', tastiness: 7 },
    { name: 'Rainbow', item: 'Variety', tastiness: 6 }
  ];

});