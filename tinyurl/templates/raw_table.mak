<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <meta charset="utf-8"/>
    <title>Go crazy!  Edit shit!</title>
    <link rel="icon" type="image/png" href="${request.static_path('tinyurl:static/pawprint.png')}" />

    <!-- Bootstrap core CSS -->
    <link href="//oss.maxcdn.com/libs/twitter-bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet"/>
    <link href="${request.static_path('tinyurl:static/sticky-footer.css')}" rel="stylesheet">

    <!-- Custom styles for this scaffold -->
    <link href="${request.static_path('tinyurl:static/theme.css')}" rel="stylesheet">

    <!-- Persona mumbo jumbo -->
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
    <script src="https://login.persona.org/include.js" type="text/javascript"></script>
    <script type="text/javascript">${request.persona_js}</script>

    <!-- handsontable -->
    <script src="//handsontable.com/dist/handsontable.full.js"></script>
    <link rel="stylesheet" media="screen" href="//handsontable.com/dist/handsontable.full.css">
    </head>

    <body>
      <div class="container-fluid">
        ${request.persona_button}
        <div class="row">
          <div class="col-md-12">
            <div class="table-responsive" id="example">
            </div>
          </div>
        </div>
      </div>
    </body>
    <script type="text/javascript">
      var data = [
      %for e in table:
      [new Date(${e.time_t * 1000}),
      "${e.human_hash}",
      "${e.long_url}"],
      %endfor
      ];

      var container = document.getElementById('example');
      var hot = new Handsontable(container, {
                                 data: data,
                                 minSpareRows: 0,
                                 rowHeaders: true,
                                 colHeaders: ["Date", "Hash", "URL"],
                                 contextMenu: true
      });
    </script>
  </html>
