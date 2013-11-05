converter = new Markdown.Converter()
editor = new Markdown.Editor(converter)
editor.run()


$("#reactionCancel").click () ->
    article_id = $("#article-id").attr("value")
    window.location("/article/#{article_id}")

