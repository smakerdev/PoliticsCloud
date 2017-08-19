var api = require('../routes/api');
module.exports = (router, connection) => {
    router.get('/', function (req, res) {

            connection.query('select * from keyword', function (error, results, fields) {
                if (error) throw error;
                var words = [];
                for (var i = 0; i < results.length; i++) {
                    words.push("text", results[i].keyword);
                }
                res.render('index', {
                    result: results,
                    words: words,
                    url: api.api_url
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