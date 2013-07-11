package sandbox

import util.Implicits._

import com.mongodb.casbah.Imports._
import util.Data.readLinesWithHeaders

object TraverCoursewareStudentmodule {
  val FileName = "src/main/resources/courses/harvardx-2013-04-07/ER22x/courseware_studentmodule_small.sql"
  val CourseName = "ER22x"
  val CollectionName = "CoursewareStudentModule"
  val MongoDatabase = MongoClient()(CourseName)
  val MongoCollection = MongoDatabase(CollectionName)

  def main(args: Array[String]) {
    readLinesWithHeaders(FileName, "\t") { (lineNumber, headers, line) =>
      assert(headers.length == line.length)
      MongoCollection += headers.zip(line).toMap
    }

    MongoCollection foreach println
    MongoDatabase.dropDatabase
  }
}
