<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>Gimme URL, You</title>
    <link rel="icon" type="image/png" href="${request.static_path('tinyurl:static/pawprint.png')}" />

    <!-- Bootstrap core CSS -->
    <link href="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet"/>

    <!-- Custom styles for this scaffold -->
    <link href="${request.static_path('tinyurl:static/theme.css')}" rel="stylesheet">
    </head>
    <body>
      <div>
        <p   style="text-align:left"><big><big><a href="/">HOME</a></big></big></p>
        <img style="float:right" src="https://img.shields.io/github/release/offby1/pyramid-tinyurl.svg"/>
      </div>
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
      <div>
        <p>Some recent entries:</p>
        <table border="1" style="font-family: monospace;">
          <tr>
            <th>Age</th>
            <th>Long</th>
            <th>Short</th>
          </tr>
          %for e in recent_entries:
          <tr>
            <td>${e['age']}</td>
            <td><a href="${e['long_url']}">${truncate(e['long_url'], 50)}</a></td>
            <td><a href="${e['short_url']}">${e['human_hash']}</a></td>
          </tr>
          %endfor
        </table>
      </div>
    </body>
  </html>
