var client_id = 'TEn6rLqKYMODIumOV_pZ';
var client_secret = '976Up3Phrl';

var auth_client_id = '8_lQw6Qglnj5oTUUGwIV';
var auth_client_secret = 'TthCJY2jIs';
var state = "success";
var redirectURI = encodeURI("http://localhost:3000/api/auth/callback");
var api_url = "";


module.exports = (router, connection) => {
    router.get('/', function (req, res) {
        res.send('Hello');
    });

    router.get('/news', function (req, res) {
            api_url = 'https://openapi.naver.com/v1/search/news?query=' + encodeURI(req.query.query) + "&display=50";
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


                    // var result = JSON.parse(body);
                    // for (var i = 0; i < result.items.length; i++) {
                    //     var data = {
                    //         title: result.items[i].title,
                    //         originallink: result.items[i].originallink,
                    //         link: result.items[i].link,
                    //         description: result.items[i].description,
                    //         pubData: result.items[i].pubData
                    //     }

                    //     var query = connection.query('INSERT INTO news SET ?', data, function (error, results, fields) {
                    //         if (error) throw error;
                    //     });
                    // }

                    res.end(body);
                } else {
                    res.status(response.statusCode).end();
                    console.log('error = ' + response.statusCode);
                }
            });
        })

        .get('/auth', function (req, res) {
            api_url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=' + auth_client_id + '&redirect_uri=' + redirectURI + '&state=' + state;
            res.render('login', {
                url: api_url
            });
            // res.writeHead(200, {
            //     'Content-Type': 'text/html;charset=utf-8'
            // });
            // res.end("<a href='" + api_url + "'><img height='50' src='http://static.nid.naver.com/oauth/small_g_in.PNG'/></a>");
        })

        .get('/auth/callback', function (req, res) {

            code = req.query.code;
            state = req.query.state;
            api_url = 'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id=' +
                auth_client_id + '&client_secret=' + auth_client_secret + '&redirect_uri=' + redirectURI + '&code=' + code + '&state=' + state;
            var request = require('request');
            var options = {
                url: api_url,
                headers: {
                    'X-Naver-Client-Id': auth_client_id,
                    'X-Naver-Client-Secret': auth_client_secret
                }
            };

            request.get(options, function (error, response, body) {
                if (!error && response.statusCode == 200) {
                    res.writeHead(200, {
                        'Content-Type': 'application/json;charset=utf-8'
                    });
                    var data = JSON.parse(body);
                    var token = data.access_token;
                    req.session.auth = token;
                    
                    res.end(body);
                    // res.end(body);
                    // return res.send("<script>alert('로그인되었습니다.');location.href('../../../');</script>")
                } else {
                    res.status(response.statusCode).end();
                    console.log('error = ' + response.statusCode);
                }
            });
        });

    return router;
}