<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <meta charset="utf-8"/>
    <title>Gimme URL, You</title>
    <link rel="icon" type="image/png" href="${request.static_path('tinyurl:static/pawprint.png')}" />

    <!-- Bootstrap core CSS -->
    <link href="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet"/>
    <link href="${request.static_path('tinyurl:static/sticky-footer.css')}" rel="stylesheet">

    <!-- Custom styles for this scaffold -->
    <link href="${request.static_path('tinyurl:static/theme.css')}" rel="stylesheet">

    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>

    <script src='https://www.google.com/recaptcha/api.js'></script>
    </head>
    <body>
      <div class="container-fluid">
        <div class="row" style="margin-bottom: 5rem; margin-left: 0%; font-size: 200%;">
          <p><a href="/">HOME</a></p>
          <a href="${github_home_page}"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://camo.githubusercontent.com/52760788cde945287fbb584134c4cbc2bc36f904/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6769746875622f726962626f6e732f666f726b6d655f72696768745f77686974655f6666666666662e706e67" alt="Fork me on GitHub" data-canonical-src="https://s3.amazonaws.com/github/ribbons/forkme_right_white_ffffff.png"></a>
        </div>
        <div class="row" style="margin-bottom: 5rem;">
          <div class="col-md-12">
            <div class="text-center">
              <form action="${request.route_url('shorten')}" method="get" style="margin-bottom: 2rem;">
                <input type="text" id="input_url" name="input_url" placeholder="Type a URL here, yo"/>
                <input type="submit" value="Tiny-ify it"/>
                <div class="g-recaptcha" data-sitekey="6LcsPBkTAAAAAC8PdjnUhN0GYVEcDACpW76G39cl"
                %if not display_captcha:
                style="display:none"
                %endif
                     ></div>
              </form>
              %if short_url:
              <div style="font-size: 200%">
                <p><strong>Dig: <a href="${short_url}">${human_hash}</a></strong></p>
              </div>
              %else:
              <div>
                <p>Your short URL will appear here.</p>
              </div>
              %endif
            </div>
          </div>
        </div>


        <div class="row">
          <div class="col-md-2">
            <p>Some recent entries:</p>
          </div>
        </div>

        <div class="row">
          <div class="col-md-12">
            <div class="table-responsive">
              <table class="table">
                <tr>
                  <th>Age</th>
                  <th>Long</th>
                  <th>Short</th>
                </tr>
                %for e in recent_entries:
                <tr>
                  <td>${e['age']}</td>
                  <td><a href="${e['long_url']}">${truncate(e['long_url'], 100)}</a></td>
                  <td style="font-family: monospace;" ><a href="${e['short_url']}">${e['human_hash']}</a></td>
                </tr>
                %endfor
              </table>
            </div>
          </div>
        </div>
        <a href="/edit">Edit this stuff</a>
      </div>
      <footer class="footer">
        <div class="container">
          <div class="text-center">
            <p class="text-muted">
              © 2015-2016 <a href="http://github.com/offby1/">This guy right here</a>
              |
              A shameless ripoff of <a href="http://tinyurl.com/">tinyurl.com</a>
              %if this_commit_url:
              |
              <a href="${this_commit_url}">Version</a>
              %endif
              |
              If you're me, you can see the underlying data <a
              href="https://us-west-1.console.aws.amazon.com/dynamodb/home?region=us-west-1#tables:selected=hashes">here</a>
            </p>
          </div>
        </div>
      </footer>
    </body>
  </html>
