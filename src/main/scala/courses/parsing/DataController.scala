package courses.parsing

import util.Implicits._
import util.Debug._

import java.io.File

import courses.DatabaseConfig

/**
 * Thrown when a DatabaseWriter is given a path that is not a directory.
 */
class PathNotDirectoryException(message: String) extends Exception(message)

/**
 * Thrown when a problem with course ID retrieval is encountered.
 */
class CourseIDException(message: String) extends Exception(message)

class DataController(dataDirPath: String) {
    /* make sure the given path represents a directory */
    val dir = new File(dataDirPath)
    if (!dir.isDirectory) {
        throw new PathNotDirectoryException(s"The given path, $dataDirPath, is not a directory.")
    }

    /* get the files in the directory in order to get the course ID */
    val fileNames = dir.listFiles map {f => f.getName}

    /* get the course ID from the filenames */
    var courseID: String = null
    DatabaseConfig.fileHandlers foreach { handler =>
        fileNames foreach { name =>
            val fileNameRegex = ("(.*)" + handler.fileName + "$").r
            name match {
                case fileNameRegex(prefix) =>
                    if (courseID == null) {
                        courseID = prefix
                    } else if (prefix != courseID) {
                        courseID = null
                        throw new CourseIDException("Two required files have different prefixes. Unable to determine course ID.")
                    }
                case _ =>
            }
        }
    }

    def processFiles() {
        DatabaseConfig.fileHandlers foreach { handler =>
            println("processing " + handler.fileName)
            handler.processFile(dataDirPath, courseID)
        }
    }
}