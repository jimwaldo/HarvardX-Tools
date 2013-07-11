package test.testing

import src.main.scala.courses.parsing._
import org.scalatest.FeatureSpec

class DataControllerSpec extends FeatureSpec {
  var testFilePath = "/cs91r-harvardx-project/src/main/resources/courses/harvardx-2013-02-25/ER22/HarvardX-ER22x-2013_Spring-auth_userprofile.sql"
  
  feature("Basic information extraction from filepath") {
    scenario("check the path of a DataController") {
      val testData = DataController(testFilePath)
      assert(testData.path === testFilePath)
    }
    
    scenario("check the course name of a DataController") {
      val testData = DataController(testFilePath)
      assert(testData.courseName === "ER22")
    }
    
    scenario("check the file name of a DataController") {
      val testData = DataController(testFilePath)
      assert(testData.fileName === "HarvardX-ER22x-2013_Spring-auth_userprofile")
    }
    
    scenario("check the file extension of a DataController") {
      val testData = DataController(testFilePath)
      assert(testData.fileExtension match {
        case SQLFile => true
        case _ => false
      })
    }
    
    scenario("check the year of a DataController") {
      val testData = DataController(testFilePath)
      assert(testData.year === "2013")
    }
    
  }
}