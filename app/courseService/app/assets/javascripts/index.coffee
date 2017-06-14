$ ->
  $.get "/courses", (courses) ->
    $.each courses, (index, course) ->
      name = $("<div>").addClass("name").text course.name
      title = $("<div>").addClass("title").text course.title
      author = $("<div>").addClass("author").text course.author
      $("#courses").append $("<li>").append(name).append(title).append(author)