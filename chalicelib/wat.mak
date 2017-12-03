<html>
    My samoyed is really hairy.
    <table class="table">
        <tr>
            <th>Created at</th>
            <th>Long</th>
            <th>Short</th>
        </tr>

        %for row in rows:
            <tr>
                <td>${row['create_date']}</td>
                <td><a href="${row['long_url']}">${row['long_url']}</a></td>
                <td style="font-family: monospace;" ><a href="${compute_short_url (row)}">${row['human_hash']}</a></td>
            </tr>
        %endfor
    </table>
</html>
