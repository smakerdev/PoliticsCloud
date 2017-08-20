var config = require('../config');
var api_url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=' + config.auth_client_id + '&redirect_uri=' + config.redirectURI + '&state=' + config.state;

module.exports = (router, connection) => {
    router.get('/', function (req, res) {
            connection.query('select * from keyword', function (error, results, fields) {
                if (error) throw error;
                res.render('index', {
                    result: results,
                    url: api_url
                });


                console.log(api_url);

            });
        })

        .get('/word/', function (req, res) {

        })

        .get('/sub/:number', function (req, res) {
            connection.query("select * from keyword where id = ?", req.params.number, function (error, results, fields) {
                if (error) throw error;
                connection.query("select * from news where keyword_id = ?", req.params.number, function (error, result, fields) {
                    if (error) throw error;
                    var data = JSON.parse(JSON.stringify(result));

                    connection.query("select * from comment where keyword_id = ?", req.params.number, function (error, comment, fields) {
                        if (error) throw error;
                        var comment_data = JSON.parse(JSON.stringify(comment));

                        res.render('sub', {
                            number: req.params.number,
                            keyword: results[0].keyword,
                            news: data,
                            comment: comment_data
                        });

                    });
                });
            });
        });

    return router;
}