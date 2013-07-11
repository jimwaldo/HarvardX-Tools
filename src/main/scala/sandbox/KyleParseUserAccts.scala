// package sandbox

// object KyleParseUserAccts extends App {
//     val CourseName = "ER22x"
//     val FileName   = "Student Course Enrollment"
//     val DataSource = "src/main/resources/courses/harvardx-2013-04-16/ER22x/HarvardX-ER22x-2013_Spring-auth_userprofile_truncated.sql"
//     val MongoCollection = MongoClient()(CourseName)(FileName)
    
//     readLinesWithHeaders(DataSource, "\t") { (lineNumber, headers, line) =>
//         MongoCollection += (for {(k, v) <- headers.zip(line)} yield (k -> v)).toMap
//     }
//     val src = Source.fromFile("../../resources/courses/harvardx-2013-04-16/ER22x/HarvardX-ER22x-2013_Spring-auth_userprofile_truncated.sql")
//     val iter = src.getLines().map(_.split(":"))
//     // print the uid for Guest
//     iter.find(_(0) == "Guest") foreach (a => println(a(2)))
//     // the rest of iter is not processed
//     src.close()

// }
