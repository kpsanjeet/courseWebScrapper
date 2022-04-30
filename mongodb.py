from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo
import json
import  logging as lg
import course

lg.basicConfig(filename = 'mongodb_log.out',level = lg.DEBUG,format='%(asctime)s %(levelname)s %(message)s')

def dataToInsert_mongodb(courseName:'str') -> 'dict':
    details = dict()
    courseName = courseName.replace(" " ,"-")
    ineuron_url = "https://courses.ineuron.ai/" + courseName
    uClient = uReq(ineuron_url)
    ineuronPage = uClient.read()
    uClient.close()
    ineuron_html = bs(ineuronPage, "html.parser")
    bigboxes = ineuron_html.find("script", {"type": "application/json"})
    courseDetails = json.loads(bigboxes.string)

    # details["title"] = courseDetails["props"]["pageProps"]["data"]["title"]
    subId = course.subCategoryId(courseDetails)
    details["category"], details["subcategory"] = course.categorySubcategory(courseDetails ,subId)

    miscObj = course.courseMisc(courseDetails)

    details["active"] = miscObj.active()
    details["isJobGuaranteeProgram"] = miscObj.isJobGuaranteeProgram()
    details["mode"] = miscObj.mode()
    details["priceIN"] = miscObj.priceIN()
    details["priceUS"] = miscObj.priceUS()
    details["courseInOneNeuron"] = miscObj.courseInOneNeuron()
    details["startDate"] = miscObj.startDate()
    details["timings"] = miscObj.timings()
    details["doubtClearing"] = miscObj.doubtClearing()
    details["language"] = miscObj.language()
    details["duration"] = miscObj.duration()
    details["certificateBenchmark"] = miscObj.certificateBenchmark()


    metaObj = course.courseMeta(courseDetails)

    details["courseDescription"] = metaObj.courseDescription()
    details["instructorsName"] = metaObj.instructorsDetails("name")
    details["instructorsEmail"] = metaObj.instructorsDetails("email")
    details["instructorsdescription"] = metaObj.instructorsDetails("description")
    details["learn"] = metaObj.learn()
    details["features"] = metaObj.features()
    details["requirements"] = metaObj.requirements()
    details["curriculum"] = metaObj.curriculum()
    details["projects"] = metaObj.projects()

    return details

coursesName = course.coursesName()
db_config = "mongodb+srv://test:******@cluster0.tjuqz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


##########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##############
# Inserting courses name and its related fields(or keys such as mode, price, projects, features etc.
with pymongo.MongoClient(db_config) as client:
    db = client["ineuron"]
    coll = db["courseDetails"]
    try:
        coll.insert_one({"coursesName": coursesName})

        fields = list(dataToInsert_mongodb(coursesName[0]).keys())
        coll.insert_one({"fields": fields})
    except:
        lg.exception("Exception Occured:")
########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#################



##########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###############################
# Inserting data for evry courses one by one
with pymongo.MongoClient(db_config) as client:
    db = client["ineuron"] # Database
    coll = db["courseDetails"] # Collection
    for cn in coursesName:
        try:
            coursedata = {cn:dataToInsert_mongodb(cn)}
            coll.insert_one(coursedata) # Inserting documents
            lg.info("Data inserted successfully into collection 'courseDetails'.")
        except:
            lg.exception("Exception Occured:")
            continue

###############%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##################

def delete_collection(db_config:'str', collection:'str' = "courseDetails", database:'str' = 'ineuron'):
    with pymongo.MongoClient(db_config) as client:
        db = client[f"{database}"]  # Database
        coll = db[f"{collection}"]  # Collection
        x = coll.delete_many({}) # Removing collection
        lg.info(f"{x.deleted_count} documents deleted from {collection}")

# delete_collection(db_config)
