A simple HTTP server
-------------------------------------
Server only accepts requests with headers that include
GET, HTTP/1.1 and Host:

Written by Megan Slater and Jesse Klein.

Invaluable input regarding tests provided by Jonathan Stallings.

Server file is configured to run with the 'webroot' folder in the same directory,
with the server's root directory inside the webroot folder. The resolve_url()
function will handle the file extensions in the webroot folder, and default to
plain text for other types.
