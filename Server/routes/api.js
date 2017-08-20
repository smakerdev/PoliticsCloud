var api_url = "";

module.exports = (router, connection, config) => {
    router.get('/', function (req, res) {
        res.send('Hello');
    });

    router.get('/news', function (req, res) {
            api_url = 'https://openapi.naver.com/v1/search/news?query=' + encodeURI(req.query.query) + "&display=50";
            var request = require('request');
            var options = {
                url: api_url,
                headers: {
                    'X-Naver-Client-Id': config.client_id,
                    'X-Naver-Client-Secret': config.client_secret
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

            
            api_url = 'https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=' + config.auth_client_id + '&redirect_uri=' + config.redirectURI + '&state=' + config.state;
            return res.redirect(api_url);
            // res.render('login', {
            //     url: api_url
            // });
            
        })

        .get('/auth/callback', function (req, res) {

            code = req.query.code;
            state = req.query.state;
            
            api_url = 'https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id=' +
                config.auth_client_id + '&client_secret=' + config.auth_client_secret + '&redirect_uri=' + config.redirectURI + '&code=' + config.code + '&state=' + config.state;
            var request = require('request');
            var options = {
                url: api_url,
                headers: {
                    'X-Naver-Client-Id': config.auth_client_id,
                    'X-Naver-Client-Secret': config.auth_client_secret
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
                } else {
                    return res.status(response.statusCode).end();
                    console.log('error = ' + response.statusCode);
                }
            });
        })

        .get('/logout', function (req, res) {
            req.session.auth = null;
            res.status(200);
            return res.send("<script>alert('로그아웃되었습니다.');location.replace('../../');</script>");
        });
    return router;
}