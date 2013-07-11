package sandbox

import com.mongodb.casbah.Imports._
import util.Implicits._
import util.Data.{readLinesWithHeaders, using}
import util.Constants.ResourceRoot

/**
 * @author Tingley
 */
object TingleyCourseEnrollment extends App {
  val CourseName = "ER22x"
  val FileName   = "Student Course Enrollment"
  val DataSource = s"$ResourceRoot/courses/harvardx-2013-04-07/ER22x/tingleysampleNOPUSH.sql"

  using(CourseName >> FileName) { (MongoCollection) => 
    readLinesWithHeaders(DataSource, "\t") { (lineNumber, headers, line) =>
      MongoCollection += (for {(k, v) <- headers.zip(line)} yield (k -> v)).toMap
    }

    /* FOR CLEANUP PURPOSES ONLY; REMOVE THE NEXT LINES! */
    println
    println(s"CREATED DATABASE $FileName")
    MongoCollection.foreach(println)
    println
    println("NOW REMOVING DATABASE")
    MongoCollection.drop
  }
}
