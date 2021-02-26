<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li><a href="#send-alert">How to send alert to the system?</a></li>
  </ol>
</details>

## How to send alert to the system?

The first thing you need to do is create a user that belongs to the "api_user" group. Then run the command below with user password that created before and take note of the output. This will be your API key.
```shell
python -c 'from hashlib import sha256;print(sha256("<API-USER-PASSWORD>".encode()).hexdigest())
```

Then, you could create alert now. Run the command below for the first alert send to the system. If you call alerts URLs without data, the system returns you a required data list.
```shell
curl -XPOST "http://localhost:8080/api/v1/alerts/" \ 
  -H "Content-Type: application/json" \
  -H "x-access-tokens: <YOUR-API-TOKEN>" \
  -d '{"message": "Test alert message body", "alias": "Test alert message alias", "source": "Enterprise Manager Console", "priority": "P3"}'
```

__Note that__; Alerts consolidate by their alias. This means, alert similarity calculates with alias and the same alert must come with the same alias.
