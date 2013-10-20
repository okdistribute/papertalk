sites = [{"name": "scholar",\
        "regex": """.*scholar.google.com\/citations\\?view_op=view_citation.*"""},
        {"name": "mendeley",\
        "regex": ".*mendeley.com.*"},
        {"name": "ssrn",\
        "regex": ".*papers.ssrn.com.*"}]

check_url = (url) ->
    sites.forEach (site) ->
        re = RegExp(site["regex"])
        if re.test(url)
            console.log(site["name"], url)
            $("#" + site["name"]).removeClass("faded")
            window.site = site["name"]
        else
            $("#" + site["name"]).addClass("faded")




$("#articleInput").keyup () ->
    text = $(this).val()
    site = check_url(text)

$("#articleGo").click () ->
    query = $("#articleInput").val()

    if site
        $.ajax "/article/url",
            type: "POST"
            data:
                site: window.site,
                url: query
            error: () ->
                alert("failed to grab article with /article/url")
            success: (data) ->
                console.log(data)
    else
        $.ajax "/article/search",
            type: "POST"
            data:
                query: query
            error: () ->
                alert("failed to grab article with /article/search")
            success: (data) ->
                console.log(data)