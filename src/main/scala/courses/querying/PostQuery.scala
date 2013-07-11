package courses.querying

import util.Implicits._
import util.Data.using
import courses.DatabaseConfig

import com.mongodb.casbah.Imports._

import collection.immutable.ListMap

sealed abstract class PostQueryOption
case object AuthorBreakdown extends PostQueryOption
case object VoteBreakdown extends PostQueryOption

object PostQuery {
    def apply(database: String) = new PostQuery(database)
}

class PostQuery(database: String) extends Query[PostQueryOption] {
    def of(query: PostQueryOption): QueryResult[String] = {
        query match {
            case AuthorBreakdown =>
                using (database >> DatabaseConfig.PostsCollectionName) { postsCollection =>
                    /* get distinct author IDs */
                    val authors = postsCollection.distinct("author_id")

                    val iterator = for (author <- authors.iterator) yield {
                        val posts = postsCollection.find(MongoDBObject("author_id" -> author))
                        ListMap(
                            "author" -> author,
                            "posts" -> posts
                        )
                    }

                    QueryResult(iterator)
                }
            case VoteBreakdown =>
                using (database >> DatabaseConfig.PostsCollectionName) { postsCollection =>
                    val mapJS = """
                        function map() {
                            emit(this.author_id, {up: this.votes.up_count, down: this.votes.down_count});
                        }
                    """

                    val reduceJS = """
                        function reduce(key, values) {
                            var counts = {up: 0, down: 0};
                            for (var i = 0; i < values.length; i++) {
                                counts.up += values[i].up;
                                counts.down += values[i].down;
                            }
                            return counts;
                        }
                    """

                    /* get distinct author IDs */
                    // val authors = postsCollection.distinct("author_id")

                    val output = postsCollection.mapReduce(mapJS, reduceJS, MapReduceInlineOutput, verbose = true)

                    val iterator = for (entry <- output) yield {
                        val values = entry.getAs[Map[String, String]]("value").get

                        ListMap(
                            "author" -> entry.getAs[String]("_id"),
                            "up" -> values("up"),
                            "down" -> values("down")
                        )
                    }

                    QueryResult(iterator)
                }
        }
    }
}