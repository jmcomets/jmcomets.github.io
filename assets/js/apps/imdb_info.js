angular.module('IMDbInfo', [])

.constant('USER_ID', 'ur25909675')

.service('API', function($http, $q, USER_ID) {
  var service = {};

  var corsProxy = 'https://cors-anywhere.herokuapp.com/';
  var rssApiUrl = corsProxy + 'http://rss.imdb.com/user/' + USER_ID;

  function rssGet(url) {
    return $http.get(rssApiUrl + url, {
      transformResponse: function(data) {
        var x2js = new X2JS();
        return x2js.xml_str2json(data);
      }
    });
  }

  function parseRatings(data) {
    var ratings = [];

    angular.forEach(data.rss.channel.item, function(item) {
      ratings.push({
        link: item.link,
        title: item.title.replace(/^(.*) \(\d+\)$/, '$1'),
        year: parseInt(item.title.replace(/^.*\((\d+)\)$/, '$1')),
        rating: parseInt(item.description.replace(/^[\s\S]*rated this (1?\d)[\s\S]*$/, '$1')),
        pubDate: item.pubDate[0].replace(/^(\w{3}, \d{2} \w{3} \d{4}).*$/, '$1')
      });
    });

    return ratings;
  }

  service.ratings = function() {
    var deferred = $q.defer();

    rssGet('/ratings').then(function(response) {
      deferred.resolve(parseRatings(response.data));
    }, function() {
      deferred.reject();
    });

    return deferred.promise;
  };

  return service;
})

.controller('RatingsController', function($scope, API) {
  $scope.ratings = [];

  API.ratings().then(function(ratings) {
    $scope.ratings = ratings;
  });

  $scope.ratingClass = function(rating) {
    if (rating < 5) {
      return 'danger';
    } else if (rating < 7) {
      return 'warning';
    } else if (rating < 9) {
      return 'info';
    } else {
      return 'success';
    }
  }
})

;
