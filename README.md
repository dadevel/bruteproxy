# bruteproxy

During internal pentests you often encounter a myriad of login portals with potentially weak passwords.
This repo contains a few scripts to automate password brute forcing with [mitmproxy](https://github.com/mitmproxy/mitmproxy/) and [ffuf](https://github.com/ffuf/ffuf)

> **Warning:** This is just a proof of concept and may be unstable 🚧

# Setup & Usage

Clone the repository.

~~~ bash
git clone --depth 1 https://github.com/dadevel/bruteproxy.git
cd ./bruteproxy
poetry install
~~~

Start the HTTP proxy.

~~~ bash
poetry run mitmdump -s ./proxy.py --no-rawtcp --no-http2 --ssl-insecure --listen-host 127.0.0.1 --listen-port 8080
~~~

Configure `http://127.0.0.1:8080` as proxy in your browser.

Submit a specific username or the string `FUZZUSER` and the password `FUZZPASS` on every login portal you encounter.
The proxy will recognize this requests and dump them into the `./logins` folder.

Generate ffuf commands for the collected requests with [ffufgen.sh](./ffufgen.sh).

~~~ bash
./ffufgen.sh -c -w ./common-usernames.txt:FUZZUSER -w ./common-usernames.txt:FUZZPASS -mode pitchfork -ac
./ffufgen.sh -c -w ./common-usernames.txt:FUZZUSER -w ./common-passwords.txt:FUZZPASS -mode clusterbomb -ac
~~~

Or build the commands manually.

~~~ bash
ffuf -request ./logins/https-example.com-443.req.txt -request-proto https -of csv -o ./logins/https-example.com-443.ffuf.csv -c -w ./common-usernames.txt:FUZZUSER -w ./common-passwords.txt:FUZZPASS -ac
~~~
