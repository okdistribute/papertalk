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
            return site
        else
            $("#" + site["name"]).addClass("faded")

        return null

$("#articleInput").keyup () ->
    text = $(this).val()
    site = check_url(text)

$("#articleGo").click () ->
    text = $("#articleInput").val()
    site = check_url(text)
    if site
        $.ajax "/article/url",
            type: "POST"
            data:
                site: site,
                url: text
            error: () ->
                alert("failed to grab article")
            success: (data) ->
                console.log(data)
    else
        $.ajax "/article/search",
            type: "GET"
            data:
                query: text
            error: () ->
                alert("failed to grab article")
            success: (data) ->
                console.log(data)