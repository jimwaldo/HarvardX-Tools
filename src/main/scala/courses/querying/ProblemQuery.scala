package courses.querying

import util.Implicits._
import util.Data.using
import courses.DatabaseConfig

import com.mongodb.casbah.Imports._

import collection.immutable.ListMap

sealed abstract class ProblemQueryOption
case object CorrectnessBreakdown extends ProblemQueryOption

object ProblemQuery {
    def apply(database: String) = new ProblemQuery(database)
}

class ProblemQuery(database: String) extends Query[ProblemQueryOption] {
    def of(query: ProblemQueryOption): QueryResult[String] = {
        query match {
            case CorrectnessBreakdown =>
                using (database >> DatabaseConfig.StudentmoduleProblemCollectionName) { problemsCollection =>
                    /* get the module IDs of the problems */
                    val problems = problemsCollection.distinct("module_id")
                    println("NUM PROBLEMS: " + problems.length)

                    val iterator = for (problem <- problems.iterator) yield {
                        val problemSlug = problem.asInstanceOf[String].replace("://", "-").replace("/", "-") + "_2_1"

                        val correct = problemsCollection.find(
                            MongoDBObject("module_id" -> problem) ++ $and("state.correct_map." + problemSlug + ".correctness" -> "correct"),
                            Query.StudentIDField)
                        val incorrect = problemsCollection.find(
                            MongoDBObject("module_id" -> problem) ++ $and("state.correct_map." + problemSlug + ".correctness" -> "incorrect"),
                            Query.StudentIDField)
                        val attempted = problemsCollection.find(
                            MongoDBObject("module_id" -> problem) ++ $and("state.attempts" $gt 0),
                            Query.StudentIDField)
                        val notAttempted = problemsCollection.find(
                            MongoDBObject("module_id" -> problem) ++ $and("state.attempts" -> 0),
                            Query.StudentIDField)

                        ListMap(
                            "probem" -> problem,
                            "correct" -> correct,
                            "incorrect" -> incorrect,
                            "attempted" -> attempted,
                            "notAttempted" -> notAttempted
                        )
                    }

                    QueryResult(iterator)
                }
        }
    }
}