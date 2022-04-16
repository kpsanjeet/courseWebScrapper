from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import json
import re

def coursesName() -> 'list':
    ineuron_url = "https://courses.ineuron.ai"
    uClient = uReq(ineuron_url)
    ineuronPage = uClient.read()
    uClient.close()
    ineuron_html = bs(ineuronPage, "html.parser")
    bigboxes = ineuron_html.find("script", {"type": "application/json"})
    coursesDetails = json.loads(bigboxes.string)
    courses = coursesDetails["props"]["pageProps"]["initialState"]["init"]["courses"]
    return list(courses.keys())


def categorySubcategory(courseDetails:'dict', subCategoryId:'str') -> 'tuple':

    categoryIds = list(courseDetails["props"]["pageProps"]["initialState"]["init"]["categories"].keys())
    for categoryId in categoryIds:
        categoryDetails = courseDetails["props"]["pageProps"]["initialState"]["init"]["categories"][categoryId]
        if subCategoryId in categoryDetails["subCategories"].keys():

            categoryTitle = categoryDetails["title"]
            SubcategoryTitle = categoryDetails["subCategories"][subCategoryId]["title"]

            return (categoryTitle, SubcategoryTitle)

def subCategoryId(courseDetails:'dict') -> 'str':
    courseData = courseDetails["props"]["pageProps"]["data"]
    return courseData["details"]["categoryId"]


class courseMisc():

    def __init__(self, courseDetails: 'dict'):
        self.dataStr = str(courseDetails["props"]["pageProps"]["data"]).replace("'", "")

    def search(self, attributeName: 'str') -> 'list':
        regex = re.compile(f"(?:{attributeName}): ([0-9A-z\s:()-]+)")
        return regex.findall(self.dataStr)

    def mode(self) -> 'str':
        return self.search("mode")[0]

    def isJobGuaranteeProgram(self) -> 'str':
        return self.search("isJobGuaranteeProgram")[0]

    def active(self) -> 'str':
        return self.search("active")[0]

    def startDate(self) -> 'str':
        get = self.search("startDate")
        if get == []:
            return "NA"
        return get[0]

    def timings(self) -> 'str':
        get1 = self.search("timings")
        get2 = self.search("classTimings")

        if get1 == [] and get2 == []:
            return "NA"

        elif get1 == []:
            return get2[0]

        else:
            return get1[0]

    def doubtClearing(self) -> 'str':
        get = self.search("doubtClearing")
        if get == []:
            return "NA"
        return get[0]

    def priceIN(self) -> 'str':
        get = self.search("IN")
        if get == []:
            return "0"
        return get[0]

    def priceUS(self) -> 'str':
        get = self.search("US")
        if get == []:
            return "0"
        return get[0]

    def courseInOneNeuron(self) -> 'str':
        get = self.search("courseInOneNeuron")
        if get == []:
            return "True"
        return get[0]

    def language(self) -> 'str':
        return self.search("language")[0]

    def certificateBenchmark(self) -> 'str':
        get = self.search("certificateBenchmark")
        if get == []:
            return "NA"
        return get[0]

    def duration(self) -> 'str':
        get = self.search("duration")
        if get == []:
            return "NA"
        return get[0]


class courseMeta():

    def __init__(self, courseDetails):
        self.courseDetails = courseDetails
        self.meta = self.meta()

    def meta(self) -> 'dict':
        courseData = self.courseDetails["props"]["pageProps"]["data"]
        if "meta" in courseData.keys():
            return courseData["meta"]
        else:
            temp = list(courseData["batches"].values())[0]
            if "meta" in temp.keys():
                return temp["meta"]

    def courseDescription(self) -> 'str':
        courseData = self.courseDetails["props"]["pageProps"]["data"]
        return courseData["details"]["description"]

    def intructorsId(self) -> 'list':
        return self.meta["instructors"]

    def instructorDetails(self, instructorId: 'str', *args: 'str') -> 'dict':
        instDetails = self.courseDetails["props"]["pageProps"]["initialState"]["init"]["instructors"][instructorId]
        return {key: instDetails[key] if key in instDetails.keys() else "NA" for key in args}

    def instructorsDetails(self, key: 'str', sep: 'str' = "\n") -> 'str':
        intructorsId = self.intructorsId()
        if len(intructorsId) > 0:
            return sep.join([self.instructorDetails(instructorId, key)[key] for instructorId in intructorsId])
        else:
            return "NA"

    def learn(self, sep: 'str' = "\n") -> 'str':
        return sep.join(self.meta["overview"]["learn"])

    def requirements(self, sep: 'str' = "\n") -> 'str':
        return sep.join(self.meta["overview"]["requirements"])

    def features(self, sep: 'str' = "\n") -> 'str':
        return sep.join(self.meta["overview"]["features"])

    def curriculum(self) -> 'dict':
        curriculum_ = {}
        for topicId in self.meta["curriculum"].keys():
            topicSylabus = []
            for topicDict in self.meta["curriculum"][topicId]["items"]:
                topicSylabus.append(topicDict["title"])
            curriculum_[self.meta["curriculum"][topicId]["title"]] = topicSylabus
        return curriculum_

    def projects(self) -> 'dict':
        projects_ = {}
        for projectId in self.meta["projects"].keys():
            projectSylabus = []
            for projectDict in self.meta["projects"][projectId]["items"]:
                projectSylabus.append(projectDict["title"])
            projects_[self.meta["projects"][projectId]["title"]] = projectSylabus
        return projects_