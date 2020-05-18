import elasticsearch from 'elasticsearch'
export default function (server) {

/**
 * This function is an example to send a search query to elasticsearch. Even though it is not used (yet) it might come 
 * handy in the future.
  async function getQueryData(client) {
    //let client;
	  client = await client.search({

      body: {
        size: 100,
        query: {
          match: {
            "user.id": '17:demostroh'
          }
        }
      },
		 index: 'session-entities'
    })
    console.log(typeof(client.hits))
    return client;
}

 */ 
  var resp
  /**
   * Establish a connection to elasticsearch.
   */
	const client = new elasticsearch.Client({
		  host: 'localhost:9200'
      });

    async function executePythonScript(minSupp,minConf){
      var skriptPath = "./plugins/customer_analytics/python/"

      var spawnSync = require("child_process").spawnSync
      var process = spawnSync('python3.7',[`associationRuleMiner.py`,`-minsupport=${minSupp}`,`-minconf=${minConf}`],{cwd: skriptPath})

      var result
      var errorMsg
      result = process.stdout.toString()
      errorMsg = process.stderr.toString()
      return result
  }

    async function executeTransformation(){
      var skriptPath = "./plugins/customer_analytics/python/"
      var spawnSync = require("child_process").spawnSync
      var process = spawnSync('python3.7', ['transform.py'] ,{cwd: skriptPath})

      var stdout = process.stdout.toString()
      var stderr = process.stderr.toString()

      return {output: stdout, error: stderr}
    }
  
  /**
   * Process the request data and execute a python script depending on the request.
   */
  server.route({
    path: '/api/customer_analytics/server/{params}',
    method: 'GET',
    handler: async function(request,h) {
      const obj = JSON.parse(JSON.stringify(request.query))
      var fs = require('fs')
      var files = fs.readdirSync('./plugins/customer_analytics/python')

      if (request.paramsArray[0] == 'associationRuleMiner.py'){

        resp = await executePythonScript(obj.minsupp,obj.minconf)
      }
      else if (request.paramsArray[0] == 'transform.py'){
        resp = await executeTransformation();
      }
      else {
        resp = await getQueryData();
      }
     
     
      return { time: (new Date()).toISOString(), data: resp }
   }
  });

}
