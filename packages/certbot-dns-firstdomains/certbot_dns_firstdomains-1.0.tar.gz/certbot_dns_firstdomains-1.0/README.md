# certbot-dns-firstdomains
First Domains DNS authenticator plugin for Certbot

An authenticator plugin for [certbot][1] to support [Let's Encrypt][2] 
DNS challenges (dns-01) for domains managed by the nameservers of [Active24][3].

This plugin is based on the [ISPConfig DNS authenticator][4] by Matthias Bilger.

## Requirements
* certbot (>=0.34.0)

_Note_: it is highly recommended that you install Certbot from PyPI (`pip install certbot`),
rather than your distribution's package manager or Snap or similar - not only is the PyPI
version usually the newest available, but there have been reports of issues with the plugin
when it's installed via PyPI and Certbot is not. If anyone has ideas on how this package
could be improved to fix these compatibility issues, please post an issue, or better yet,
a pull request - any input or help is much appreciated!

## Installation
1. First install the plugin:
   ```shell
   pip install certbot-dns-firstdomains
   ```

2. Configure it with your First Domains credentials:
   ```shell
   sudo $EDITOR /etc/letsencrypt/firstdomains.ini
   ```
   Paste the following into the configuration file:
   ```
   certbot_dns_firstdomains:dns_firstdomains_username = "your username"
   certbot_dns_firstdomains:dns_firstdomains_password = "your password"
   ```

3. Make sure the file is only readable by root! Otherwise all your domains might be in danger:
   ```shell
   sudo chmod 0600 /etc/letsencrypt/firstdomains.ini
   ```

## Usage
Request new certificates via a certbot invocation like this:

```shell
sudo certbot certonly -a certbot-dns-firstdomains:dns-firstdomains -d sub.domain.tld -d *.wildcard.tld
```

Renewals will automatically be performed using the same authenticator and credentials by certbot.

## Command Line Options
```
 --certbot-dns-firstdomains:dns-firstdomains-credentials PATH_TO_CREDENTIALS
                        Path to First Domains account credentials INI file 
                        (default: /etc/letsencrypt/firstdomains.ini)

 --certbot-dns-firstdomains:dns-firstdomains-propagation-seconds SECONDS
                        The number of seconds to wait for DNS record changes
                        to propagate before asking the ACME server to verify
                        the DNS record. Default 300.
```

## Removal

```shell
sudo pip uninstall certbot-dns-firstdomains
```

## Development

When releasing a new version, commit all changes, create an appropriate Git tag, and then run
`./release.sh` from the project directory. This will check and prepare your environment,
push the latest code to GitHub, build the distribution package and upload it to PyPI.


[1]: https://certbot.eff.org/
[2]: https://letsencrypt.org/
[4]: https://github.com/m42e/certbot-dns-ispconfig
