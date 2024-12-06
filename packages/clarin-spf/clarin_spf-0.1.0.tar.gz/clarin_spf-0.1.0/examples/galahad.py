import requests

from clarin_spf import clarin_login


def main():
    """Retrieve the user and corpora information from the Galahad portal."""
    base_url = "https://portal.clarin.ivdnt.org/galahad"
    cookies = clarin_login(base_url)
    user_resp = requests.get(f"{base_url}/api/user", cookies=cookies).json()
    corpora_resp = requests.get(f"{base_url}/api/corpora", cookies=cookies).json()

    print(f"Available corpora for user account: {user_resp['id']}")
    for corpus in corpora_resp:
        print(f"Corpus: {corpus['name']} - Public: {corpus['public']} - sourceName: {corpus['sourceName']}")


if __name__ == "__main__":
    main()
