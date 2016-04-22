import pymongo

conn = None; 

d = dict();

try: 
    conn = pymongo.MongoClient();
    print "Success";
except pymongo.errors.ConnectionFailure, e: 
    print "faile to connect %s" % e;
    sys.exit();

db = conn.pyDB;
#res = db.clusters.find({"clusterType" : "SPLUNK-IDX-OPS", "operationalStatus" : "ACTIVE"}, {"deviceRoleConfigs.deviceRole" : 1, "deviceRoleConfigs.roleConfig" : 1});
res = db.clusters.find(
    {
        "$and" : [
            {"$or" : [
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
    {"deviceRoleConfigs.deviceRole" : 1, "deviceRoleConfigs.roleConfig" : 1}
);

for i in res:
    for j in i['deviceRoleConfigs']: 
        roleConfig = j['roleConfig'];
        deviceRole = j['deviceRole'];
        if deviceRole in d: 
            d[deviceRole].add(roleConfig);
        else: 
            d[deviceRole] = set(); 
            d[deviceRole].add(roleConfig);

print "role to roleConfig: ";
#print d;
for key in d.keys():
    print key, "=>", d.get(key); 

apd = dict();

for key in d.keys():
    if key not in apd:
        apd[key] = set();
    val = d.get(key);
    for rc in val:
        n = db.roleconfigs.find({"name" : rc}, {"applicationProfiles.name" : 1, "applicationProfiles.checks" : 1});
        for ap in n:
            temp = ap['applicationProfiles'];
            for name in temp:
                apn = name['name'];
                #print name['checks'];
                apd[key].add(apn);

print "role to AP: "
#print apd;
for key in apd.keys():
    print key, "=>", apd.get(key); 

chkd = dict();

for key in apd.keys():
    if key not in chkd:
        chkd[key] = set();
    val = apd.get(key);
    for ap in val:
        chk = db.applicationprofile_monitoring.find({"applicationprofile_ref" : ap}, {"monitorchecks.type" : 1});
        for item in chk:
            temp = item.get('monitorchecks');
            if temp == None:
                continue;
            for t in temp:
                type = t['type'];
                chkd[key].add(type);

print "role to checks: ";
for key in chkd.keys():
    print key, "=>", chkd.get(key);
