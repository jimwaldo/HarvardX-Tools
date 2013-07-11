package util

import java.sql._

/**
* Contains some utility functions not necessarily directly related to the project.
*
* @author Traver, Tingley
*/
object Util {
  def getTimestamp() = new java.sql.Timestamp(System.currentTimeMillis())
}
