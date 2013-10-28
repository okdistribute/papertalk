converter = new Markdown.Converter()
editor = new Markdown.Editor(converter)
editor.run()

$("#reactionSave").click () ->
    title = $("#reaction-title").val()
    text = $("#wmd-input").val()
    article_id = $("#article-id").text()
    $.ajax "/reaction/new",
        type: "POST"
        data:
            title: title,
            text: text,
            article_id: article_id
        error: () ->
            alert("failed to save article")
        success: (data) ->
            console.log(data)

$("#reactionCancel").click () ->
	console.log("not implemented")

