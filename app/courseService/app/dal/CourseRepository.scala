package dal

import javax.inject.{ Inject, Singleton }
import play.api.db.slick.DatabaseConfigProvider
import slick.driver.JdbcProfile

import models.Course

import scala.concurrent.{ Future, ExecutionContext }

/**
 * A repository for course.
 *
 * @param dbConfigProvider The Play db config provider. Play will inject this for you.
 */
@Singleton
class CourseRepository @Inject()(dbConfigProvider: DatabaseConfigProvider)(implicit ec: ExecutionContext) {
  // We want the JdbcProfile for this provider
  private val dbConfig = dbConfigProvider.get[JdbcProfile]

  // These imports are important, the first one brings db into scope, which will let you do the actual db operations.
  // The second one brings the Slick DSL into scope, which lets you define the table and other queries.
  import dbConfig._
  import driver.api._

  /**
   * Here we define the course table.
   */
  private class CourseTable(tag: Tag) extends Table[Course](tag, "course") {

    /** The ID column, which is the primary key, and auto incremented */
    def id = column[Long]("id", O.PrimaryKey, O.AutoInc)

    /** The name column */
    def name = column[String]("name")

    /** The title column */
    def title = column[String]("title")

    /** The author column */
    def author = column[String]("author")

    /**
     * This is the tables default "projection".
     *
     * It defines how the columns are converted to and from the Person object.
     *
     * In this case, we are simply passing the id, name and page parameters to the Course case classes
     * apply and unapply methods.
     */
    def * = (id, name, title, author) <> ((Course.apply _).tupled, Course.unapply)
  }

  /**
   * The starting point for all queries on the people table.
   */
  private val course = TableQuery[CourseTable]

  /**
   * Create a course with the given name, author, and title.
   *
   */
  def create(name: String, title: String, author: String): Future[Course] = db.run {
    // We create a projection of just the name and age columns, since we're not inserting a value for the id column
    (course.map(c => (c.name, c.title, c.author))
      // Now define it to return the id, because we want to know what id was generated for the person
      returning course.map(_.id)
      // And we define a transformation for the returned value, which combines our original parameters with the
      // returned id
      into ((desc, id) => Course(id, desc._1, desc._2, desc._3))
    // And finally, insert the course into the database
    ) += (name, title, author)
  }

  /**
   * List all the courses in the database.
   */
  def list(): Future[Seq[Course]] = db.run {
    course.result
  }
}
