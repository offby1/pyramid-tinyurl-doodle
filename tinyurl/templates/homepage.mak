<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Gimme URL, You</title>
    <!-- Bootstrap core CSS -->
    <link href="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this scaffold -->
    <link href="${request.static_path('tinyurl:static/theme.css')}" rel="stylesheet">
  </head>
  <body>
    <form action="/shorten/" method="get">
      <label for="input_url">URL To Make Tiny</label>
      <input type="text" id="input_url" name="input_url" placeholder="Type a URL here, yo"/>
      <br/>
      <input type="submit" value="Tiny-ify it"/>
    </form>
    %if short_url:
    <div>
    <p>Dig: <a href="${short_url}">${short_url}</a></p>
    </div>
    %else:
    <div>
    <p>Your short URL will appear here.</p>
    </div>
    %endif
  </body>
</html>
