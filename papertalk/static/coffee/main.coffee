sites = [{"name": "scholar",\
        "regex": """.*scholar.google.com\/citations\\?view_op=view_citation.*"""},
        {"name": "mendeley",\
        "regex": ".*mendeley.com.*"},
        {"name": "pdf",\
        "regex": """http.*\.pdf"""},
        {"name": "ssrn",\
        "regex": ".*ssrn.com.*"}]

check_url = (url) ->
    success = false
    url_destination = false
    sites.forEach (site) ->
        re = new RegExp(site.regex)
        if re.test(url)
            # url
            $("#" + site.name).removeClass("faded")
            success = true
            url_destination = site.name
        else
            # search
            $("#" + site.name).addClass("faded")

    if success
      console.log("url")
      $("#articleForm").attr("action", "/article/url")
      $("#siteInput").attr("value", url_destination)
    else
      console.log("search")
      $("#articleForm").attr("action", "/article/search/1")



$("#articleInput").keyup () ->
    text = $(this).val()
    check_url(text)
