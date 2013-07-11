package sandbox

import com.mongodb.casbah.Imports._
import scala.io.Source.fromFile

/**
 * @author Rafic
 */
object StudentCourseEnrollment extends App {
  val DataFile = "src/main/resources/courses/harvardx-2013-04-07/ER22x/spring-student-course-enrollment.sql"
   
  val mongoClient = MongoClient()
  val mongoDB = mongoClient("casbah_test")("test_data")
  
  val lines = fromFile(DataFile).getLines()
  val fields = lines.next().split("\t")
  
  for (line <- lines) {
    val newObj = MongoDBObject()
    for ((field, value) <- fields.zip(line.split("\t"))) {
      newObj += (field -> value)
    }
    mongoDB += newObj
  }
  
  mongoDB.foreach(println)
  mongoDB.dropCollection()
}
