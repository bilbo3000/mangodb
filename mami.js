var m = db.clusters.find({"clusterType" : "AJNA", "operationalStatus" : "ACTIVE"}, {"deviceRoleConfigs.deviceRole" : true, "deviceRoleConfigs.roleConfig" : true});
// var roles = m.map(function(c) {return c.deviceRoleConfigs});

m.forEach(function (x) {
    x.deviceRoleConfigs.forEach(
        function(y) {
            // printjson(y.roleConfig), // name of the role config
            var n = db.roleconfigs.find({"name" : y.roleConfig}, {"applicationProfiles" : true}).pretty()
            n.forEach(
                function(i) {
                    i.applicationProfiles.forEach(
                        function(j) {
                            // printjson(j.name), // name of the application profile
                            var chk = db.applicationprofile_monitoring.find({"applicationprofile_ref" : j.name}, {"monitorchecks.type" : true})
                            chk.forEach(
                                function(k) {
                                    print(y.deviceRole + "=")
                                    // printjson(y.deviceRole)
                                    printjson(k.monitorchecks)
                                }
                            )
                        }    
                    )
                }
            )
        }
    )
} )


