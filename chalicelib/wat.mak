<html>
    My samoyed is really hairy.
    <table class="table">
        <tr>
            <th>Age</th>
            <th>Long</th>
            <th>Short</th>
        </tr>

        %for row in rows:
            <tr>
                <td>${row['create_date']}</td>
                <td><a href="${row['long_url']}">${row['long_url']}</a></td>
                <td style="font-family: monospace;" ><a>${row['human_hash']}</a></td>
            </tr> 
        %endfor
    </table>
</html>
