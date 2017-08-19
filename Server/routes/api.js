var client_id = 'TEn6rLqKYMODIumOV_pZ';
var client_secret = '976Up3Phrl';

module.exports = (router, connection) => {
    router.get('/', function (req, res) {
        res.send('Hello');
    });

    router.get('/news', function (req, res) {
        var api_url = 'https://openapi.naver.com/v1/search/news?query=' + encodeURI(req.query.query) + "&display=50";
        var request = require('request');
        var options = {
            url: api_url,
            headers: {
                'X-Naver-Client-Id': client_id,
                'X-Naver-Client-Secret': client_secret
            }
        };
        request.get(options, function (error, response, body) {
            if (!error && response.statusCode == 200) {
                res.writeHead(200, {
                    'Content-Type': 'application/json;charset=utf-8'
                });

                var result = JSON.parse(body);
                for (var i = 0; i < result.items.length; i++) {
                    var data = {
                        title: result.items[i].title,
                        originallink: result.items[i].originallink,
                        link: result.items[i].link,
                        description: result.items[i].description,
                        pubData: result.items[i].pubData
                    }
    
                    var query = connection.query('INSERT INTO news SET ?', data, function (error, results, fields) {
                        if (error) throw error;
                    });
                }

                res.end(body);
            } else {
                res.status(response.statusCode).end();
                console.log('error = ' + response.statusCode);
            }
        });
    });

    return router;
}