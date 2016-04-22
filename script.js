// var res = db.clusters.find({"clusterType" : "AJNA", "operationalStatus" : "ACTIVE"}, {id : true});
var res = db.clusters.find(
    {
        $and : [
            {$or : [
                {"clusterType" : "AJNA"}, 
                {"clusterType" : "SPLUNK-WEB"},
                {"clusterType" : "SPLUNK-API"},
                {"clusterType" : "SPLUNK-UI-SHARED"},
                {"clusterType" : "SPLUNK-UI"},
                {"clusterType" : "SPLUNK-IDX"},
                {"clusterType" : "SPLUNK-IDX-OPS"},
                {"clusterType" : "GRAPHITE-STORAGE"}
            ]}, 
            {"operationalStatus" : "ACTIVE"}
        ]
    }, 
    {id : true}
);
var ids = res.map(function(c){return c.id});
//var hosts = db.allhosts.find({"cluster" : {$in:ids}}, {name : true, deviceRole : true}).map(function(c) {return c.name});
var hosts = db.allhosts.find({"cluster" : {$in:ids}}, {name : true, deviceRole : true}).map(function(c) {return c.name});
//var roles = db.allhosts.distinct("deviceRole" , {"name" : {$in : hosts}});
//printjson(roles)
printjson(hosts)
