package util

import java.io.FileWriter

import util.Implicits._
import util.Constants._
import util.Debug._

import scala.collection.mutable.{Map => mMap}
import scala.io.Source
import scala.io.Source.fromFile
import com.mongodb.casbah.Imports._

sealed abstract class SourceType[+utilType] {
  type UtilizerType = utilType
}
case class FileReadSource(filename: String) extends SourceType[Iterator[String]]
case class FileAppendSource(filename: String) extends SourceType[FileWriter]
case class ScalaIOSource(source: Source) extends SourceType[Iterator[String]]
case class MongoCollectionSource(databaseName: String, collectionName: String)
    extends SourceType[MongoCollection]

/**
 * This class is used to provide helper methods and DSL for processing data.
 * For instance, this class can be used to provide scaffolding for working
 * with files, databases, and stream processing.
 *
 * Implicit functions dealing with data transforming should also be placed here.
 *
 * @author Tingley, Traver
 */
object Data {
  /**
   * Maintains a list of all Mongo collections used so that they can be rolled 
   * back after the program terminates.
   */
  val mongoCollectionsUsed: mMap[MongoCollectionSource, List[DBObject]] = 
    mMap[MongoCollectionSource, List[DBObject]]()

  /**
   * Scaffolding for reading from a source, executing a block of code, and 
   * ensuring that the source is closed when done.
   * 
   * @param source    The source to read.
   * @param block     The block of code to run. This is passed an iterator for
   *                  the lines of the source.
   *
   * @return Whatever the user's code block returns (ignore this if you don't
   *         need it).
   */
  def using[ReturnType](source: SourceType[Any]) (
    block: (source.UtilizerType) => ReturnType
  ): ReturnType = {
    source match {
      case FileReadSource(filename) =>
        val source = fromFile(filename)
        try{
          return block(source.getLines)
        } finally source.close()

      case FileAppendSource(filename) =>
        val fileWriter = new FileWriter(filename, true)
        try {
          block(fileWriter)
        } finally fileWriter.close() 

      case ScalaIOSource(source) => return block(source.getLines)
      case source@MongoCollectionSource(database, coll) =>
        val collection = MongoClient()(database)(coll)

        if (RollbackMode && !mongoCollectionsUsed.contains(source)) {
          mongoCollectionsUsed += (source -> (collection toList))
        }

        return block(collection)
    }
  }

  /**
   * 
   */
  // def readFromCSV(source: SourceType[Iterator[String]], splitter: '\t') (
  //   block: () => Unit
  // ) {
  //   // TODO
  // }

  /**
   * Reads lines from a source according to some splitter, and executes a user-
   * provided function for each line. It first parses the header (the first line
   * of the source), and then passes to the user's function the split header 
   * values along with the split line values for each line.
   *
   * @param source    The source to read from.
   * @param splitter  The delimiter used to separate columns of the source.
   * @param block     The user-provided function to execute for each line of the
   *                  source. Will pass to the user the current line number, the
   *                  splitter-delimited headers, and the splitter-delimited 
   *                  line values.
   */
  def readLinesWithHeaders(source: SourceType[Iterator[String]], splitter: String) (
    block: (Int, Array[String], Array[String]) => Unit
  ) {
    source match {
      case FileReadSource(filename) =>
        val source = fromFile(filename)
        try{
          /* force evaluation of the iterator so the foreach is executed */
          return collectLinesWithHeaders(source, splitter)(block) foreach identity
        } finally {
          source.close()
        }
      case ScalaIOSource(source) =>
        /* force evaluation of the iterator so the foreach is executed */
        return collectLinesWithHeaders(source, splitter)(block) foreach identity
    }
  }

  /**
   * Reads lines from a source according to some splitter, and executes a user-
   * provided function for each line. Produces an iterator over the outputs of 
   * the user-defined function. It first parses the header (the first line
   * of the source), and then passes to the user's function the split header 
   * values along with the split line values for each line.
   *
   * @param source    The source to read from.
   * @param splitter  The delimiter used to separate columns of the source.
   * @param block     The user-provided function to execute for each line of the
   *                  source. Will pass to the user the current line number, the
   *                  splitter-delimited headers, and the splitter-delimited 
   *                  line values.
   *
   * @return Iterator over the output of the user-defined function.
   */
  def collectLinesWithHeaders[ReturnType](source: Source, splitter: String) (
    block: (Int, Array[String], Array[String]) => ReturnType
  ): Iterator[ReturnType] = {
      val lines = source getLines
      val header = lines.next split splitter
      
      for {(line, lineNumber) <- lines zipWithIndex}
        yield block(lineNumber + 1, header, line split(splitter, -1))
  }

  /**
   * Reads lines from a source according to some splitter, and executes a user-
   * provided function for each entry of each line. It first parses the header 
   * (the first line of the source), and then passes to the user's function each 
   * line value along with its corresponding header, for each line.
   *
   * @param source    The source to read from.
   * @param splitter  The delimiter used to separate columns of the source.
   * @param block     The user-provided function to execute for each entry of 
   *                  each line of the source. Will pass to the user the current 
   *                  line number, the header corresponding to the current line
   *                  value, and the current line value.
   */
  def readEntriesWithHeaders(source: SourceType[Iterator[String]], splitter: String) (
    block: (Int, String, String) => Unit
  ) {
    readLinesWithHeaders(source, splitter) { (lineNumber, headers, line) =>
      for {(header, entry) <- headers zip line} block(lineNumber, header, entry)
    }
  }

  /**
   * Reads lines from a source according to some splitter, and executes a user-
   * provided function for each entry of each line. Produces an iterator over 
   * the outputs of the user-defined function. It first parses the header (the 
   * first line of the source), and then passes to the user's function each line 
   * value along with its corresponding header, for each line, collects the 
   * results into an iterator, and returns them.
   *
   * @param source    The source to read from.
   * @param splitter  The delimiter used to separate columns of the source.
   * @param block     The user-provided function to execute for each entry of 
   *                  each line of the source. Will pass to the user the current 
   *                  line number, the header corresponding to the current line
   *                  value, and the current line value.
   *
   * @return Iterator over the output of the user-defined function.
   */
  def collectEntriesWithHeaders[ReturnType](source: Source, splitter: String)(
    block: (Int, String, String) => ReturnType
  ): Iterator[ReturnType] =
    collectLinesWithHeaders(source, splitter) { (lineNumber, headers, line) =>
      for {(header, entry) <- headers zip line} 
        yield block(lineNumber, header, entry)
    } flatMap identity
}
