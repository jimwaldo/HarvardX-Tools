package courses.parsing

import java.io.File
import scala.io.Source.fromFile
import scala.util.parsing.json.JSON
import scala.collection.mutable.{Map => mMap}
import com.mongodb.casbah.Imports._

import util.Implicits._
import util.Data.using
import util.Debug._

/**
 * Thrown when FileHandler is given a file of an unknown format.
 */
class UnknownFileTypeException(message: String) extends Exception(message)

/**
 * Thrown when a FileHandler subclass is given a file of a type that it cannot handle.
 */
class UnsupportedFileTypeException(message: String) extends Exception(message)

abstract class FileHandler(val fileName: String, collectionName: String, fieldsToRemove: List[String] = List()) {
    def processFile(path: String, courseID: String)

    /**
     * Removes fields (keys) from the given mutable map.
     */
    def removeFields(map: mMap[String, _ <: Any]) {
        fieldsToRemove foreach { field => map -= field }
    }

    /**
     * Get the extension of fileName.
     */
    private def getExtension(): String = {
        val i = fileName.lastIndexOf('.')
        if (i >= 0) fileName.substring(i + 1) else ""
    }

    /**
     * Convert a file extension (String) into a FileFormat.
     */
    def getFileFormat: FileFormat = {
        getExtension match {
            case "sql" => SQLFile
            case "xml" => XMLFile
            case "mongo" => MongoFile
            case _ => UnknownFile
        }
    }
}

class BasicFileHandler(fileName: String, collectionName: String, fieldsToRemove: List[String] = List())
        extends FileHandler(fileName, collectionName, fieldsToRemove) {
    def processFile(path: String, courseID: String) {
        val fullFileName = new File(path, courseID + fileName).getAbsolutePath()
        val source = fromFile(fullFileName)

        try {
            using(courseID >> collectionName) { (mongoCollection) =>
                getFileFormat match {
                    case SQLFile =>
                        SQLParser.parse(source) foreach { mapOption =>
                            mapOption match {
                                case Some(map) =>
                                    /* remove fields that we don't need to store */
                                    removeFields(map)

                                    /* add the document to the collection */                            
                                    mongoCollection += map
                                case None =>
                            }
                        }
                    case XMLFile =>
                        throw new UnsupportedFileTypeException("XML file handling is not yet supported.")
                    case MongoFile =>
                        MongoParser.parse(source) foreach { map =>
                            // TODO make removeFields(map) work; MongoParser currently returns an immutable map

                            mongoCollection += map
                        }
                    case UnknownFile =>
                        throw new UnknownFileTypeException("Unknown file type!")
                }
            }
        } finally {
            source.close()
        }
        
    }
}

class StudentModuleFileHandler(fileName: String, collectionName: String, fieldsToRemove: List[String] = List())
        extends FileHandler(fileName, collectionName, fieldsToRemove) {
    def processFile(path: String, courseID: String) {
        val fullFileName = new File(path, courseID + fileName).getAbsolutePath()
        val source = fromFile(fullFileName)

        val database = MongoClient()(courseID)
        var collections = mMap[String, MongoCollection]()

        try {
            getFileFormat match {
                case SQLFile =>
                    SQLParser.parse(source) foreach { mapOption =>
                        mapOption match {
                            case Some(map) =>
                                val moduleType = map("module_type").toString
                                if (!collections.contains(moduleType)) {
                                    collections += moduleType -> database(collectionName + "_" + moduleType)
                                }

                                /* remove fields that we don't need to store */
                                removeFields(map)

                                /* add the document to the collection */
                                collections(moduleType) += map
                            case None =>
                        }
                    }
                case XMLFile =>
                    throw new UnsupportedFileTypeException("XML file handling is not yet supported.")
                case MongoFile =>
                    throw new UnsupportedFileTypeException("StudentModuleFileHandler doesn't support .mongo files.")
                case UnknownFile =>
                    throw new UnknownFileTypeException("Unknown file type!")
            }
        } finally {
            source.close()
        }

    }
}