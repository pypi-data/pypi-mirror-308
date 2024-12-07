# @hint: xmltodict (channel=pypi)
import xmltodict
# @hint: requests (channel=pypi)
import requests

import zlib
from concurrent.futures import ThreadPoolExecutor
import re
import struct

def fetch_sitemap(url, timeout=15000, retries=0, debug=False, reject_unauthorized=True, lastmod=0, proxy_agent=None, exclusions=None):
    exclusions = exclusions or []

    def is_gzip(data):
        return len(data) > 2 and struct.unpack("H", data[:2])[0] == 0x8b1f

    def parse_sitemap(sitemap_url):
        try:
            response = requests.get(sitemap_url, timeout=timeout / 1000, verify=reject_unauthorized)
            response.raise_for_status()

            if is_gzip(response.content):
                content = zlib.decompress(response.content, zlib.MAX_WBITS | 16)
            else:
                content = response.content

            parsed_data = xmltodict.parse(content.decode())
            return parsed_data

        except requests.RequestException as e:
            return {"error": str(e), "data": None}
        except zlib.error as e:
            return {"error": f"Decompression failed: {str(e)}", "data": None}

    def fetch_robots_txt(base_url):
        robots_url = f"{base_url.rstrip('/')}/robots.txt"
        try:
            response = requests.get(robots_url, timeout=5)
            response.raise_for_status()
            sitemap_urls = []
            for line in response.text.splitlines():
                line = line.strip()
                if line.lower().startswith("sitemap:"):
                    sitemap_urls.append(line.split(":", 1)[1].strip())
            if debug:
                print(f"Discovered sitemaps in robots.txt: {sitemap_urls}")
            return sitemap_urls
        except requests.RequestException as e:
            if debug:
                print(f"Failed to fetch robots.txt from {robots_url}: {e}")
            return []

    def filter_sites(sites):
        filtered_sites = []
        for site in sites:
            if 'loc' not in site:
                continue
            if lastmod and 'lastmod' in site:
                modified = int(re.sub(r"[-:T]", "", site['lastmod']))
                if modified < lastmod:
                    continue
            if any(pattern.search(site['loc']) for pattern in exclusions):
                continue
            filtered_sites.append(site['loc'])
        return filtered_sites

    def crawl(url, attempt=0):
        parsed_data = parse_sitemap(url)
        if parsed_data.get("error"):
            if attempt < retries:
                if debug:
                    print(f"Retrying {url} ({attempt + 1}/{retries}) due to error: {parsed_data['error']}")
                return crawl(url, attempt + 1)
            return {"sites": [], "errors": [{"type": "RequestError", "message": parsed_data["error"], "url": url}]}

        if 'urlset' in parsed_data:
            sites = parsed_data['urlset'].get('url', [])
            sites = sites if isinstance(sites, list) else [sites]
            return {"sites": filter_sites(sites), "errors": []}

        if 'sitemapindex' in parsed_data:
            sitemaps = parsed_data['sitemapindex'].get('sitemap', [])
            sitemaps = sitemaps if isinstance(sitemaps, list) else [sitemaps]
            sitemap_urls = [s['loc'] for s in sitemaps if 'loc' in s]
            results = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(crawl, sm_url) for sm_url in sitemap_urls]
                for future in futures:
                    results.append(future.result())

            all_sites = []
            all_errors = []
            for result in results:
                all_sites.extend(result.get("sites", []))
                all_errors.extend(result.get("errors", []))

            return {"sites": all_sites, "errors": all_errors}

        return {"sites": [], "errors": [{"type": "ParseError", "message": "Invalid sitemap structure", "url": url}]}

    # Try fetching sitemaps from robots.txt
    robots_sitemaps = fetch_robots_txt(url)
    if robots_sitemaps:
        # Crawl all discovered sitemaps from robots.txt
        all_results = []
        for sitemap_url in robots_sitemaps:
            all_results.append(crawl(sitemap_url))

        # Combine results from all sitemaps
        combined_sites = []
        combined_errors = []
        for result in all_results:
            combined_sites.extend(result["sites"])
            combined_errors.extend(result["errors"])
        return {"url": url, "sites": combined_sites, "errors": combined_errors}

    # Fallback to crawling the provided URL directly
    result = crawl(url)
    return {"url": url, "sites": result["sites"], "errors": result["errors"]}

def default(**kwargs):
    return fetch_sitemap(**kwargs)

# if __name__ == "__main__":
#     result = default(
#         url="https://www.gry.pl",
#         timeout=15000,
#         retries=3,
#         debug=True,
#         exclusions=[re.compile(r"https://1001spiele.de/private.*")]
#     )
#     print(result)
