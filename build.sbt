scalaVersion := "2.10.1"

libraryDependencies ++= 
  List(
    "com.github.tototoshi" %% "scala-csv" % "0.8.0",
    "org.scalatest" % "scalatest_2.10" % "1.9.1" % "test",
    "org.mongodb" %% "casbah" % "2.6.1",
    "com.github.scopt" %% "scopt" % "2.1.0",
    "org.slf4j" % "slf4j-simple" % "1.7.5"
  )

resolvers += "sonatype-public" at "https://oss.sonatype.org/content/groups/public"

scalacOptions ++= 
  Seq(
    "-unchecked",
    "-deprecation",
    "-feature",
    "-language:postfixOps",
    "-language:implicitConversions"
  )