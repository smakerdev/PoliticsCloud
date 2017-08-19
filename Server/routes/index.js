var config = require('../config');
var api_url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=' + config.auth_client_id + '&redirect_uri=' + config.redirectURI + '&state=' + config.state;

module.exports = (router, connection) => {
    router.get('/', function (req, res) {
            connection.query('select * from keyword', function (error, results, fields) {
                if (error) throw error;
                var words = [];
                for (var i = 0; i < results.length; i++) {
                    words.push("text", results[i].keyword);
                }

                console.log(api_url);
                res.render('index', {
                    result: results,
                    words: words,
                    url: api_url
                });
            });
        })

        .get('/login', function (req, res) {
            
        })

        .post('./logincheck', function (req, res) {

        })

        .get('/register', function (req, res) {

        })

        .get('/word/', function (req, res) {

        })

        .get('/sub/:number', function (req, res) {
            connection.query("select * from keyword where id = ?", req.params.number, function (error, results, fields) {
                if (error) throw error;
                res.render('sub', {
                    number: req.params.number,
                    keyword: results[0].keyword
                });
            });
        });

    return router;
}