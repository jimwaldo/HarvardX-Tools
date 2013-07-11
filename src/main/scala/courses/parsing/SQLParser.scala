package courses.parsing

import util.Implicits._
import util.Data.collectLinesWithHeaders
import scala.io.Source
import scala.collection.mutable.{Map => mMap}

object SQLParser extends Parser[Option[mMap[String, Any]]] {
    def parse(source: Source): Iterator[Option[mMap[String, Any]]] = {
        collectLinesWithHeaders(source, "\t") { (lineNum, headers, line) =>
            if (headers.length == line.length) {
                Some(headers.zip(line).toMap.convertJSONFields)
            } else {
                None
            }
        }
    }
}
