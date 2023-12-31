<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <meta charset="utf-8"/>
    <title>Gimme URL, You</title>
    <link rel="icon" type="image/png" href="${request.static_path('tinyurl:static/pawprint.png')}" />

    <!-- Bootstrap core CSS -->
    <link href="//cdn.jsdelivr.net/npm/bootstrap@5.0.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-CuOF+2SnTUfTwSZjCXf01h7uYhfOBuxIhGKPbfEJ3+FqH/s6cIFN9bGr1HmAg4fQ" crossorigin="anonymous">
    <link href="${request.static_path('tinyurl:static/sticky-footer.css')}" rel="stylesheet">

    <!-- Custom styles for this scaffold -->
    <link href="${request.static_path('tinyurl:static/theme.css')}" rel="stylesheet">

    <script src='https://www.google.com/recaptcha/api.js'></script>
    </head>
    <body>
      <div class="container-fluid">
        <div class="row" style="margin-bottom: 5rem; margin-left: 0%; font-size: 200%;">
          <p><a href="/">HOME</a></p>

          <!-- **** Begin Fork-Me-On-Gitlab-Ribbon-HTML. See MIT License at https://gitlab.com/seanwasere/fork-me-on-gitlab **** -->
          <a href="${gitlab_home_page}">
            <span style="font-family: tahoma; font-size: 20px; position:fixed; top:50px; right:-45px; display:block; -webkit-transform: rotate(45deg); -moz-transform: rotate(45deg); background-color:red; color:white; padding: 4px 30px 4px 30px; z-index:99">Fork Me On GitLab</span>
          </a>
          <!-- **** End Fork-Me-On-Gitlab-Ribbon-HTML **** -->

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
          <div class="col-md-12">
            <p>Some recent entries (out of about ${approximate_table_size} total) :</p>
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
              © 2015-2024 <a href="https://gitlab.com/offby1/">This guy right here</a>
              |
              A shameless (but nicer-looking) ripoff of <a href="http://tinyurl.com/">tinyurl.com</a>
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
      <script src="//cdn.jsdelivr.net/npm/bootstrap@5.0.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-popRpmFF9JQgExhfw5tZT4I9/CI5e2QcuUZPOVXb1m7qUmeR2b50u+YFEYe1wgzy" crossorigin="anonymous"></script>
    </body>
  </html>
