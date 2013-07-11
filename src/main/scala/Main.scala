import java.io.File

import scopt.mutable.OptionParser

import courses.parsing.DataController
import util.Data._
import util.Constants._
import util.Debug._

/**
 * Main control object. Minimal business logic should be placed here.
 */
object Main {
  /**
   * Main entry point of the program. Use the -h flag for information about 
   * command line arguments.
   *
   * @param args Use the -h flag for help with the command line arguments.
   */
  def main(args: Array[String]) {
    /* Define the command line args. */
    case class Config(var directory: String = "")
    var config = Config()
    val parser = new OptionParser("EdXDataTool") {
      arg(
        "directory",
        "the directory containing the files to import",
        {s: String => config.directory = s}
      )
    }

    initialize()
    
    try {
      /* parse the command line args */
      if (parser.parse(args)) {
        log("PROGRAM RUN")
        val controller = new DataController(config.directory)
        controller.processFiles
      } else {
        log("PROGRAM FAILED DUE TO INVALID COMMAND LINE ARGUMENTS")
      }
    } finally cleanUp()
  }

  /**
   * Called once at the beginning of each run of the program. Only called if the
   * program was passed valid command line arguments.
   */
  def initialize() {
    /* Delete the existing log file. */
    new File(TempLogFile).delete
  }

  /**
   * Executes clean-up operations after execution has completed.
   */
  def cleanUp() {
    /* Rollback databases that we modified by dropping each used collection and 
     * rebuild it. */
    for ((source, entries) <- mongoCollectionsUsed) {
      debugLog(s"Cleaning up $source")
      using(source) { collection =>
        collection.dropCollection
        entries.foreach { collection += _ }
      }
    }

    log("PROGRAM EXITING")
  }
}
