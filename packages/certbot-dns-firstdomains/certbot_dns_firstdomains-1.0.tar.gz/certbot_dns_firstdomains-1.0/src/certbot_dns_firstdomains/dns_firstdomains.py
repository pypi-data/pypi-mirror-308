from certbot.plugins.dns_common import DNSAuthenticator
from requests.sessions import Session
from functools import cache


class Authenticator(DNSAuthenticator):
    """First Domains Authenticator."""

    description = "First Domains Authenticator"
    user_agent = "certbot/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credentials = None
        self.session = Session()

    @classmethod
    def add_parser_arguments(cls, add):
        super().add_parser_arguments(add, default_propagation_seconds=300)
        add(
            "credentials",
            help="First Domains credentials INI file.",
            default="/etc/letsencrypt/firstdomains.ini",
        )

    def more_info(self):
        return "First Domains Authenticator"

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "First Domains credentials INI file",
            {
                "username": "Username for First Domains",
                "password": "Password for First Domains",
            },
        )
        self.login()

    def _perform(self, domain, validation_name, validation):
        self.add_dns_txt(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        self.remove_dns_txt(domain, validation)

    def login(self):
        login_url = "https://1stdomains.nz/client/login.php"
        data = {
            "action": "login",
            "account_login": self.credentials.conf("username"),
            "account_password": self.credentials.conf("password"),
        }
        headers = {"User-Agent": self.user_agent}
        response = self.session.post(login_url, data=data, headers=headers)
        response.raise_for_status()  # Raise an error if the request failed
        return None

    def add_dns_txt(self, domain: str, record_name: str, txt_value: str):
        root_name = self.get_root_name(domain)
        self.add_record(record_name, txt_value, root_name)

    def remove_dns_txt(self, domain: str, txt_value: str):
        root_name = self.get_root_name(domain)
        record_id = self.get_record_id(txt_value, root_name)
        if record_id:
            self.remove_record(record_id, root_name)

    @cache
    def get_root_name(self, record_name: str):
        # Determine the root domain name by trying various subdomains
        parts = record_name.split(".")
        for i in range(len(parts) - 2, -1, -1):
            current_name = ".".join(parts[i:])
            if self.check_domain_exists(current_name):
                return current_name
        return None

    def check_domain_exists(self, domain_name: str):
        url = "https://1stdomains.nz/client/json_wrapper.php"
        data = {
            "library": "zone_manager",
            "action": "load_records",
            "domain_name": domain_name,
        }
        headers = {
            "Referer": "https://1stdomains.nz/client/account_manager.php",
            "User-Agent": self.user_agent,
        }
        response = self.session.post(url, data=data, headers=headers)
        response.raise_for_status()
        return "errors" not in response.json()

    def add_record(self, record_name: str, txt_value: str, root_name: str):
        url = "https://1stdomains.nz/client/json_wrapper.php"
        data = {
            "library": "zone_manager",
            "action": "add_record",
            "domain_name": root_name,
            "host_name": record_name,
            "record_type": "TXT",
            "record_content": txt_value,
        }
        headers = {
            "Referer": "https://1stdomains.nz/client/account_manager.php",
            "User-Agent": self.user_agent,
        }
        response = self.session.post(url, data=data, headers=headers)
        response.raise_for_status()

    def get_record_id(self, txt_value: str, root_name: str):
        url = "https://1stdomains.nz/client/json_wrapper.php"
        data = {
            "library": "zone_manager",
            "action": "load_records",
            "domain_name": root_name,
        }
        headers = {
            "Referer": "https://1stdomains.nz/client/account_manager.php",
            "User-Agent": self.user_agent,
        }
        response = self.session.post(url, data=data, headers=headers)
        response.raise_for_status()
        records = response.json().get("rows", [])
        for record in records:
            if record["cell"][3] == txt_value:
                return record["cell"][0]
        return None

    def remove_record(self, record_id: str, root_name: str):
        url = "https://1stdomains.nz/client/json_wrapper.php"
        data = {
            "library": "zone_manager",
            "action": "del_records",
            "domain_name": root_name,
            "checked_records": record_id,
        }
        headers = {
            "Referer": "https://1stdomains.nz/client/account_manager.php",
            "User-Agent": self.user_agent,
        }
        response = self.session.post(url, data=data, headers=headers)
        response.raise_for_status()
