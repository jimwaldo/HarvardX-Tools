package courses.querying

import com.mongodb.casbah.Imports._

import collection.immutable.ListMap

sealed abstract class QueryAddon
case object Country extends QueryAddon

sealed abstract class QueryOperation
case object Count extends QueryOperation

sealed abstract class QueryResultFormat
case object CSV extends QueryResultFormat
case object XML extends QueryResultFormat

object QueryResult {
    def apply[T](result: Iterator[ListMap[T, Any]]): QueryResult[T] = new QueryResult(result)
}

class QueryResult[T](val result: Iterator[ListMap[T, Any]]) {
    def by(addon: QueryAddon): QueryResult[T] = {
        addon match {
            case Country =>
                QueryResult(result)
        }
    }

    def andOutputAs(format: QueryResultFormat): Iterator[String] = {
        format match {
            case CSV =>
                /* get the headers */
                val first = result.next
                val headersMap = first map { entry =>
                    val (key, value) = entry
                    key -> key
                }

                /* add the headers to the iterator */
                val iterator = Iterator(headersMap, first) ++ result

                /* generate the CSV strings */
                for (map <- iterator) yield {
                    var contentLineList = List[String]()
                    map foreach { entry =>
                        val (key, value) = entry
                        contentLineList = contentLineList :+ value.toString
                    }
                    contentLineList mkString ", "
                }
            case XML => ???
        }
    }

    def and(operation: QueryOperation) = {
        operation match {
            case Count =>
                val iterator = for (map <- result) yield {
                    map map { entry =>
                        val (key, value) = entry

                        /* we can only get the count if the value is a MongoCursor */
                        if (value.isInstanceOf[MongoCursor]) key -> value.asInstanceOf[MongoCursor].count
                        else key -> value
                    }
                }
                QueryResult(iterator)
        }
    }
}