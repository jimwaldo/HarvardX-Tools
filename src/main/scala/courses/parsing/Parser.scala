package courses.parsing

import scala.io.Source

trait Parser[T] {
    def parse(source: Source): Iterator[T]
}