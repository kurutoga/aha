package models

import play.api.libs.json._

case class Course(id: Long, name: String, title: String, author: String)

object Course {

  implicit val courseFormat = Json.format[Course]
}
