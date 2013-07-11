package util

import scala.io.Source
import scala.collection.mutable.{Map => mMap}
import scala.util.parsing.json.JSON

/**
 * Contains all the implicit conversions used in this project. This file should
 * be imported in its entirety, i.e. via import util.Implicits._.
 *
 * @author Tingley
 */
final object Implicits {
  implicit def stringToFileReadSource(string: String): FileReadSource = FileReadSource(string)

  implicit def sourceToScalaIOSource(source: Source): ScalaIOSource = ScalaIOSource(source)

  implicit class MongoDataSpec(val database: String) extends AnyVal {
    def >>(collection: String) = MongoCollectionSource(database, collection)
  }

  class JSONMap(map: Map[String, String]) {
    /**
     * Converts fields that are string representations of JSON into
     * a map, so that the fields are accessible to Mongo.
     */
    def convertJSONFields(): mMap[String, Any] = {
        var newMap = mMap[String, Any]()
        for ((k, v) <- map) {
            JSON.parseFull(v.mkString) match {
                case Some(jsonMap) => newMap(k) = jsonMap
                case None => newMap(k) = v
            }
        }

        newMap
    }
  }
  implicit def mapToJSONMap(map: Map[String, String]) = new JSONMap(map)

}