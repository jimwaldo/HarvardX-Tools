package util

import java.io.FileWriter

import util.Data.using
import util.Implicits._
import util.Constants._
import util.Util.getTimestamp

/**
 * Contains procedures related to internal logging, debugging, and maintenance.
 *
 * @author Tingley
 */
object Debug {
  /**
   * This method allows printing and logging for future examination and 
   * debugging. This will only be printed to stdout if the constant DebugMode is
   * enabled.
   * 
   * @param message   The message to be logged.
   * @param enabled   If set to false, this debugLog statement will be 
   *                  effectively disabled. This allows debug statements to be
   *                  turned off without introducing significant code clutter.
   */
  def debugLog(message: String, enabled: Boolean = true) {
    if (enabled) {
      createLogEntry(TempLogFile, message)
      if (DebugMode) println(message)
      log(s"DEBUG: $message")
    }
  }

  /**
   * This method creates a log entry for the given message by appending the 
   * message to the file specified by the constant LogFile.
   *
   * @param message The message to be logged.
   */
  def log(message: String) {
    createLogEntry(LogFile, getTimestamp + ": " + message)
  }

  /**
   * Logs a message to the specified file by appending to the file, first
   * creating the file if it does not already exist.
   *
   * @param message  The message to be logged.
   * @param filepath The path of the log file to be appended to.
   */
  private def createLogEntry(filepath: String, message: String) {
    using(FileAppendSource(filepath)) { file =>
      file.write(message + "\n")
    }
  }
}
