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
    <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
    <script src="https://login.persona.org/include.js" type="text/javascript"></script>
    <script type="text/javascript">${request.persona_js}</script>

    <!-- datatables -->
    <style type="text/css" title="currentStyle">@import "//cdn.datatables.net/1.10.4/css/jquery.dataTables.min.css";</style>
    <style type="text/css" > table {font-family: Monospace;} </style>
    <script type="text/javascript" src="//cdn.datatables.net/1.10.4/js/jquery.dataTables.min.js"></script>

    </head>

    <body>
      <div class="container-fluid">
        <p><a href="/">HOME</a></p>
        ${request.persona_button}
        <div class="row">
          <div class="col-md-12">
            <div class="table-responsive">
              <table id="index" class="table table-bordered display" >
                <thead>
                <tr>
                  <th>Date</th>
                  <th>Hash</th>
                  <th>Url</th>
                  <th>Nix</th>
                </tr>
                </thead>
                <tbody>
                %for e in table:
                <tr>
                  <td>${e.create_date_with_tz}</td>
                  <td>${e.human_hash}</td>
                  <td>${e.long_url}</td>
                  <td>
                  <button type="button" data-delete-url="${request.route_path('delete', human_hash=e.human_hash)}">
                    Click Me to delete ${e.human_hash}!
                  </button>
                  </td>
                </tr>
                %endfor
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    <script type="text/javascript">
       $( "#index tbody" ).on( "click", "button", function() {
         nix_row( $( this ) )
       });

      var nix_row = function (button) {
        var delete_url = button.data ('deleteUrl');

         $.ajax ({
         url: delete_url,
         type: "DELETE",
         dataType: "json",
         success: function (json) {
         var table = $('#index').DataTable();

         table
           .row( button.parents('tr') )
           .remove()
           .draw();
         },
         error: function( xhr, status, errorThrown ) {
           alert( "Sorry, there was a problem!" );
           console.log( "Error: " + errorThrown );
           console.log( "Status: " + status );
           console.dir( xhr );
         }
         });
      };
      $(document).ready(function() {
      $("#index").dataTable({

       "order": [] // use whatever order the rows come back from the db

        // TODO -- add some magic whereby we can sort the table by the
        // _length_ of the long URL, since spammy URLs tend to be short.

      });
      }
      );
    </script>
    </body>
  </html>
