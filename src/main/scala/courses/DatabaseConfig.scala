package courses

import courses.parsing.{BasicFileHandler, StudentModuleFileHandler}

object DatabaseConfig {
    /* collection names for files that are imported into single collections */
    val UserCollectionName = "users"
    val UserprofileCollectionName = "userprofile"
    val CertificatesCollectionName = "certificate"
    val EnrollmentCollectionName = "enrollment"
    val PostsCollectionName = "posts"

    /* Collection names for studentmodule files, which are broken
     * up into different collections based on the module_type field.
     * StudentmoduleBaseCollectionName is used in a FileHandler below,
     * but the vals that add a string onto StudentmoduleBaseCollectionName
     * are defined here just to provide constants for use in querying code. */
    val StudentmoduleBaseCollectionName = "studentmodule"
    val StudentmoduleChapterCollectionName = StudentmoduleBaseCollectionName + "_chapter"
    val StudentmoduleCourseCollectionName = StudentmoduleBaseCollectionName + "_course"
    val StudentmodulePollCollectionName = StudentmoduleBaseCollectionName + "_poll_question"
    val StudentmoduleProblemCollectionName = StudentmoduleBaseCollectionName + "_problem"
    val StudentmoduleSequentialCollectionName = StudentmoduleBaseCollectionName + "_sequential"

    /* the files that we need to build a database for a course */
    val fileHandlers = List(
        new BasicFileHandler("-auth_user.sql", UserCollectionName, List("password")),
        // new BasicFileHandler("-auth_userprofile.xml", UserprofileCollectionName), // commented out for now because of lack of XML parsing support
        new BasicFileHandler("-certificates_generatedcertificate.sql", CertificatesCollectionName),
        new StudentModuleFileHandler("-courseware_studentmodule.sql", StudentmoduleBaseCollectionName),
        new BasicFileHandler("-student_courseenrollment.sql", EnrollmentCollectionName),
        new BasicFileHandler(".mongo", PostsCollectionName)
    )
}