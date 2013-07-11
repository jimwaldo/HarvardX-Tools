package sandbox

/* using the Java (NOT Scala) Mongo driver in this file */
import com.mongodb.MongoClient
import com.mongodb.BasicDBObject
import com.mongodb.QueryBuilder

import scala.util.parsing.json.JSON
import scala.collection.mutable.{Map => mMap}
import scala.collection.JavaConversions._

import courses.querying._

object ER22 {
    def main(args: Array[String]) {
        // val result = CertificateQuery("HarvardX-CS50x-2012") of StatusBreakdown by Country
        // result foreach println

        // val result = ProblemQuery("HarvardX-ER22x-2013_Spring") of CorrectnessBreakdown by Country and Count andOutputAs CSV
        // val result = ProblemQuery("HarvardX-CS50x-2012") of CorrectnessBreakdown by Country and Count andOutputAs CSV

        // val result = PostQuery("HarvardX-ER22x-2013_Spring") of AuthorBreakdown and Count andOutputAs CSV
        val result = PostQuery("HarvardX-ER22x-2013_Spring") of VoteBreakdown andOutputAs CSV

        // result foreach println
        result.result foreach println
        // println(result.result)
    }
}