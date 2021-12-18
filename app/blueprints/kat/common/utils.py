import markdown2

import mod_wsgi

def generate_help():
    output = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <style type="text/css">
"""
    with open('app/static/markdown.css', 'r') as f:
        output += f.read()

    output += """
</style>
</head>

<body>
"""
    output += mod_wsgi.process_group
    output += markdown2.markdown_path('README.md', extras=["code-color", "tables", "fenced-code-blocks"])
    output += """
</body>

</html>
"""
    return output
