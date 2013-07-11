package courses.parsing

/**
* FileFormat is subclassed for each possible file format of the
* data, and is sealed so we can ensure matches are exhaustive.
*/
sealed abstract class FileFormat
case object SQLFile extends FileFormat
case object XMLFile extends FileFormat
case object MongoFile extends FileFormat
case object UnknownFile extends FileFormat