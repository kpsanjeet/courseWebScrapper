from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
import  logging as lg
import mysql.connector as conn
import course

# log file
lg.basicConfig(filename = 'mysql_log.out',level = lg.DEBUG,format='%(asctime)s %(levelname)s %(message)s')

def dataToInsert_mysql(courseName: 'str') -> 'tuple':
    courseName = courseName.replace(" ", "-")
    ineuron_url = "https://courses.ineuron.ai/" + courseName
    uClient = uReq(ineuron_url)
    ineuronPage = uClient.read()
    uClient.close()
    ineuron_html = bs(ineuronPage, "html.parser")
    bigboxes = ineuron_html.find("script", {"type": "application/json"})
    courseDetails = json.loads(bigboxes.string)

    title = courseDetails["props"]["pageProps"]["data"]["title"]
    subId = course.subCategoryId(courseDetails)
    category, subcategory = course.categorySubcategory(courseDetails, subId)

    miscObj = course.courseMisc(courseDetails)

    active = miscObj.active()
    isJobGuaranteeProgram = miscObj.isJobGuaranteeProgram()
    mode = miscObj.mode()
    priceIN = miscObj.priceIN()
    priceUS = miscObj.priceUS()
    courseInOneNeuron = miscObj.courseInOneNeuron()
    startDate = miscObj.startDate()
    timings = miscObj.timings()
    doubtClearing = miscObj.doubtClearing()
    language = miscObj.language()
    duration = miscObj.duration()
    certificateBenchmark = miscObj.certificateBenchmark()

    metaObj = course.courseMeta(courseDetails)

    courseDescription = metaObj.courseDescription()
    instructorsName = metaObj.instructorsDetails("name")
    instructorsEmail = metaObj.instructorsDetails("email")
    instructorsdescription = metaObj.instructorsDetails("description")
    learn = metaObj.learn()
    features = metaObj.features()
    requirements = metaObj.requirements()

    row = (title, category, subcategory, mode, active, isJobGuaranteeProgram,
           courseInOneNeuron, priceIN, priceUS, startDate, timings, doubtClearing,
           instructorsName, instructorsEmail, instructorsdescription, courseDescription,
           language, duration, certificateBenchmark, learn, features, requirements)
    return row


def insertData(dataToInsert:'list', table:'str' = 'courseDetails',  database:'str' = 'ineuronCourses'):
    try:
        db = conn.connect(host = '127.0.0.1',
                          database = database,
                          user = 'root',
                          password = '******')

        query = f"""INSERT INTO ineuronCourses.{table}
                                                     (
                                                     title ,
                                                     category ,
                                                     subcategory ,
                                                     mode ,
                                                     active ,
                                                     isJobGuaranteeProgram ,
                                                     courseInOneNeuron ,
                                                     priceIN ,
                                                     priceUS ,
                                                     startDate ,
                                                     timings ,
                                                     doubtClearing ,
                                                     instructorsName ,
                                                     instructorsEmail ,
                                                     instructorsdescription ,
                                                     courseDescription ,
                                                     language ,
                                                     duration ,
                                                     certificateBenchmark ,
                                                     learn ,
                                                     features ,
                                                     requirements
                                                     )
                                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                               """

        cursor = db.cursor()
        cursor.executemany(query, dataToInsert)
        db.commit()
        lg.info(cursor.rowcount, f"Record inserted successfully into {table} table")


    except:
        lg.exception("An Exception Occured:")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            lg.info("MySQL connection is closed")


def dropTable(table: 'str' = 'test', database: 'str' = 'ineuronCourses'):
    try:
        db = conn.connect(host='127.0.0.1',
                          database=database,
                          user='root',
                          password='misc')
        c = db.cursor()
        c.execute(f"drop table {table}")
        db.commit()
        lg.info(f"Table {table} has droped Sucessfully.")
    except:
        lg.exception("An Exception Occured:")

    finally:
        if db.is_connected():
            c.close()
            db.close()
            lg.info("MySQL connection is closed")

# creating a database and a table
try:
    db = conn.connect(host = '127.0.0.1',user = 'root' ,passwd = "misc" )
    cursor = db.cursor()
    try:
        cursor.execute("create database ineuronCourses")
        lg.info("Database has created Successfully.")
    except:
        lg.exception("An Exception Occured:")
    query = """create table ineuronCourses.courseDetails
                                (
                                 title VARCHAR(100) ,
                                 category VARCHAR(100)  ,
                                 subcategory VARCHAR(100) ,
                                 mode VARCHAR(20) ,
                                 active VARCHAR(20),
                                 isJobGuaranteeProgram VARCHAR(20) ,
                                 courseInOneNeuron VARCHAR(20) ,
                                 priceIN VARCHAR(20) ,
                                 priceUS VARCHAR(20) ,
                                 startDate VARCHAR(100) ,
                                 timings VARCHAR(100),
                                 doubtClearing VARCHAR(200) ,
                                 instructorsName VARCHAR(200) ,
                                 instructorsEmail VARCHAR(200) ,
                                 instructorsdescription VARCHAR(2000) ,
                                 courseDescription VARCHAR(2000) ,
                                 language VARCHAR(30) ,
                                 duration VARCHAR(20) ,
                                 certificateBenchmark VARCHAR(20) ,
                                 learn VARCHAR(3000) ,
                                 features VARCHAR(3000) ,
                                 requirements VARCHAR(1000)
                                 )
            """

    #cursor.execute("create table in database ineuronCourses")
    cursor.execute(query)
    db.commit()
    lg.info(f"Table courseDetails has created Successfully database ineuronCourses.")
except:
    lg.exception("An Exception Occured:")

finally:
    if db.is_connected():
        cursor.close()
        db.close()
        lg.info("MySQL connection is closed")


# List of courses
coursesName = course.coursesName()
dataToInsert = [dataToInsert_mysql(CN) for CN in coursesName]

# Isert data into database
insertData(dataToInsert)

# dropTable("courseDetails")
