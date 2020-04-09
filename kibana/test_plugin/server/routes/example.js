import elasticsearch from 'elasticsearch'
export default function (server) {


async function getQueryData() {
    let test;
	  test = await client.search({

		 //q: query,
      body: {
        size: 100,
        query: {
          match: {
            "userid.keyword": '17:demostroh'
          }
        }
      },
		 index: 'logstash'
		})/*.then(function (body) {
      console.log(body.hits.hits[0]._source) // hier gehts weiter mit widget.widget & zeit und über da wo die 0 steht muss ich iterieren
      //test = body;
		}, function (error) {
			console.trace(error.message);
    });
    */
    console.log(test);
    console.log("juhu")

    /*
    return new Promise(resolve => {
      resolve(test);
    })
    */
    return test;
}

  var resp;
	const client = new elasticsearch.Client({
		  host: 'localhost:9200'
		  //log: 'trace'
      });
      
  server.route({
    path: '/api/test_plugin/example',
    method: 'GET',
  /*
    handler(req, reply) {
      reply({ time: (new Date()).toISOString() });
    }
    */
   handler: async function(request,h) {

    resp = await getQueryData();
/*
	  client.search({

		 //q: query,
      body: {
        query: {
          match: {
            "userid.keyword": '17:demostroh'
          }
        }
      },
		 index: 'logstash'
		}).then(await function (body) {
      //resp = body.hits.hits;
      console.log(body);
      resp = body;
		}, function (error) {
			console.trace(error.message);
    });
    */
      //console.log(resp)
    //return 'JAWOLL ALDER'
    console.log(resp)
     console.log("maaaaaaaaaaaaaan ey")
     return { time: (new Date()).toISOString(), data: resp }
   }
  });

}
