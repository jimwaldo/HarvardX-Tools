package courses.querying

import collection.immutable.ListMap

import com.mongodb.casbah.Imports._

object Query {
    /* used to tell calls to find to only return the user_id of each document */
    val UserIDField = MongoDBObject("user_id" -> 1) ++ MongoDBObject("_id" -> 0)

    /* used to tell calls to find to only return the student_id of each document */
    val StudentIDField = MongoDBObject("student_id" -> 1) ++ MongoDBObject("_id" -> 0)
}

trait Query[T] {
    def of(query: T): QueryResult[String]
}