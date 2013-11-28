sites = [{"name": "scholar",\
        "regex": """.*scholar.google.com\/citations\\?view_op=view_citation.*"""},
        {"name": "mendeley",\
        "regex": ".*mendeley.com.*"},
        {"name": "pdf",\
        "regex": """http://*.pdf"""},
        {"name": "ssrn",\
        "regex": ".*ssrn.com.*"}]

check_url = (url) ->
    sites.forEach (site) ->
        re = RegExp(site.regex)
        articleForm = $("#articleForm")
        siteField = $("#siteInput")
        if re.test(url)
            # url
            console.log("url", site.name, url)
            articleForm.attr("action", "/article/url")
            $("#" + site.name).removeClass("faded")
            siteField.attr("value", "unknown")
        else
            # search
            console.log("search", url)
            articleForm.attr("action", "/article/search")
            $("#" + site.name).addClass("faded")
            siteField.attr("value", site.name)


$("#articleInput").keyup () ->
    text = $(this).val()
    check_url(text)
