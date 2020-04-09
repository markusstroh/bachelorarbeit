import elasticsearch from 'elasticsearch'

export default function (server) {

	const client = new elasticsearch.Client({
		  host: 'localhost:9200',
		  log: 'trace'
			});


  server.route({
    path: '/api/test_plugin/search_test/{searchterm}',
    method: 'GET',
    handler(req, reply) {
      const query =  req.params.searchterm;
	  client.search({

		 q: query,
     /* body: {
        query: {
          match: {
            userid: '*stroh*'
          }
        }
      },*/
		 index: 'logstash'
		}).then(function (body) {
			var hits = body.hits.hits;
		}, function (error) {
			console.trace(error.message);
		});
	    console.log("fick dich du dumme scheiße")
			reply({ response: body.hits.hits });
		}



	  });

}
