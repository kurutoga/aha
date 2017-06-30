
name := """courseService"""

version := "1.0-SNAPSHOT"

lazy val `root` = (project in file(".")).enablePlugins(PlayScala)

scalaVersion := "2.11.11"

libraryDependencies += evolutions

libraryDependencies ++= Seq( cache , ws   , specs2 % Test,
                             "com.typesafe.play" %% "play-slick" % "2.0.2", "com.h2database" % "h2" % "1.4.194", filters )

libraryDependencies += "com.typesafe.play" %% "play-slick-evolutions" % "2.0.2"

