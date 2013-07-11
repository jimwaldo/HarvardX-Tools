package courses.parsing

import util.Implicits._

import scala.io.Source
import com.mongodb.casbah.Imports._
import com.mongodb.util.JSON

object MongoParser extends Parser[DBObject] {
    def parse(source: Source): Iterator[DBObject] = {
        for {line <- source.getLines}
            /* parse the JSON-represented BSON */
            yield JSON.parse(line).asInstanceOf[DBObject]
    }
}