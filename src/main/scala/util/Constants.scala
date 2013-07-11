package util

import scala.io.Source.fromFile

/**
 * Contains symbolic constants for use throughout the program. Ultimately, these
 * should simply provide default values, and the actual, configurable values 
 * should be offloaded as a JSON object to a user-configurable config file.
 *
 * @author Tingley
 */
object Constants {
  /* Constants for Debugging */
  val DebugMode = true
  val RollbackMode = false


  /* Constants for Paths and Files */
  val DebugRoot = "src/debug"
  val TempLogFile = s"$DebugRoot/TempLogFile.log"
  val LogFile = s"$DebugRoot/LogFile.log"
  val MainRoot = "src/main"
  val ResourceRoot = s"$MainRoot/resources"
}
