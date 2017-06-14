package controllers

import play.api._
import play.api.mvc._
import play.api.i18n._
import play.api.data.Form
import play.api.data.Forms._
import play.api.data.validation.Constraints._
import play.api.libs.json.Json
import models._
import dal._

import scala.concurrent.{ ExecutionContext, Future }

import javax.inject._

class CourseController @Inject()(repo: CourseRepository, val messagesApi: MessagesApi)
                                (implicit ec: ExecutionContext) extends Controller with I18nSupport{

  /**
   * The mapping for the course form.
   */
  val courseForm: Form[CreateCourseForm] = Form {
    mapping(
      "name" -> nonEmptyText,
      "title" -> nonEmptyText,
      "author" -> nonEmptyText
    )(CreateCourseForm.apply)(CreateCourseForm.unapply)
  }

  /**
   * The index action.
   */
  def index = Action { implicit request =>
    Ok(views.html.index(courseForm))
  }

  /**
   * The add course action.
   *
   * This is asynchronous, since we're invoking the asynchronous methods on PersonRepository.
   */
  def addCourse = Action.async { implicit request =>
    courseForm.bindFromRequest.fold(
      errorForm => {
        Future.successful(Ok(views.html.index(errorForm)))
      },
      // There were no errors in the from, so create the course.
      course => {
        repo.create(course.name, course.title, course.author).map { _ =>
          // If successful, we simply redirect to the index page.
          Redirect(routes.CourseController.index)
        }
      }
    )
  }

  /**
   * A REST endpoint that gets all the courses as JSON.
   */
  def getCourses = Action.async {
  	repo.list().map { course =>
      Ok(Json.toJson(course))
    }
  }
}

/**
 * The create course form.
 *
 * Generally for forms, you should define separate objects to your models, since forms very often need to present data
 * in a different way to your models.  In this case, it doesn't make sense to have an id parameter in the form, since
 * that is generated once it's created.
 */
case class CreateCourseForm(name: String, title: String, author: String)
