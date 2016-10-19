var app = angular.module('materializeApp', ['ui.materialize','chart.js'])
    .controller('BodyController', ["$scope", '$http', function ($scope,$http) {

        $http.get("/api/mostplayed").then(function(response) {
            $scope.mostplayed = response.data;
        });
        $http.get("/api/mostplayedweek").then(function(response) {
            $scope.mostplayedweek = response.data;
        });
        $http.get("/api/activity").then(function(response) {
            var d = moment().subtract(24, 'hours');
            var labels = [];
            for(var t=0; t<24; t++){
                labels.push(d.format("H"));
                d = d.add(1, 'hours');
            }
            $scope.activity = {
                labels: labels,
                series: ['Activity'],
                data: response.data,
                dataset: {
                    backgroundColor: "#444444",
                    hoverBackgroundColor: "#505050",
                    label: "Activity"
                },
                options: {
                    scales: {
                      yAxes: [
                        {
                          id: 'y-axis-1',
                          type: 'linear',
                          display: false,
                          position: 'left',
                          ticks: {
                            beginAtZero:true
                            }
                        }
                      ]
                    }
                  }
            };
        });

    }]);