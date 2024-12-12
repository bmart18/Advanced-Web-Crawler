import scrapy
from scrapy.crawler import CrawlerProcess
import sublist3r
import requests
import json
import os
import csv
import time
from urllib.parse import urljoin, urlparse
import datetime
import builtwith
import whois
import dns.resolver

class SiteCrawler(scrapy.Spider):
    name = "site_crawler"

    def __init__(self, start_url, *args, **kwargs):
        super(SiteCrawler, self).__init__(*args, **kwargs)
        # Ensure the start_url has the proper scheme
        if not start_url.startswith(('http://', 'https://')):
            start_url = 'https://' + start_url
        self.start_urls = [start_url]  # Start crawling from the given URL
        self.domain = urlparse(start_url).netloc  # Extract domain from the given URL
        self.visited_pages = set()  # Set to keep track of visited pages
        self.page_count = 0  # Counter to estimate the number of pages crawled
        self.subdomains = []  # Store subdomains found
        self.whois_info = {}  # Store Whois information
        self.start_time = time.time()  # Record start time for crawling
        self.summary_data = []  # Store final summary data

    def parse(self, response):
        # Check if the response status is not successful
        if response.status in [400, 404, 410]:
            self.log(f"Ignoring response with status {response.status}: {response.url}")
            return

        # Normalize URL to avoid duplicates due to different formatting
        normalized_url = urlparse(response.url)._replace(query="", fragment="").geturl()

        # Add URL to visited set and count
        if normalized_url not in self.visited_pages:
            self.visited_pages.add(normalized_url)  # Mark the page as visited
            self.page_count += 1  # Increment the page count
            self.log(f"Visited: {response.url}")

        # Follow links to other pages within the same domain
        for href in response.css('a::attr(href)').extract():
            # Ignore mailto links and other non-http schemes
            if href.startswith(('mailto:', 'tel:', 'javascript:')):
                continue

            # Skip URLs with query parameters that could lead to duplicates or dynamically generated content
            if '?' in href:
                continue

            # Normalize the URL
            href = urljoin(response.url, href)
            parsed_href = urlparse(href)

            # Ensure the link has a proper scheme (http or https)
            if parsed_href.scheme not in ('http', 'https'):
                continue

            # Skip URLs that point to documents or images
            if parsed_href.path.endswith(('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar')):
                continue

            # Check if the link is internal (contains the domain)
            if self.domain in parsed_href.netloc:
                # Skip pagination or dynamic content links that could cause loops
                if any(param in href for param in ['page=', 'next', 'sort=', 'filter=']):
                    continue
                yield response.follow(href, callback=self.parse)  # Follow the link and parse the next page

    def closed(self, reason):
        # Log the total number of pages found after crawling is complete
        self.log(f"Estimated total number of pages: {self.page_count}")
        print(f"Estimated total number of pages: {self.page_count}")
        # Perform additional operations after crawling is done
        self.get_subdomains()  # Get subdomains of the domain
        self.get_cms_info()  # Detect CMS used by the domain
        self.get_whois_info()  # Perform Whois lookup for the domain
        # Print final summary
        self.print_final_summary()
        # Write final summary to CSV
        self.write_summary_to_csv()

    def get_subdomains(self):
        # Start subdomain enumeration using Sublist3r
        self.log("Starting subdomain enumeration...")
        print("Starting subdomain enumeration...")
        self.subdomains = sublist3r.main(self.domain, 40, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
        if self.subdomains:
            subdomains_str = ', '.join(self.subdomains)
            self.log(f"Subdomains found: {subdomains_str}")
            print(f"Subdomains found: {subdomains_str}")
        else:
            self.log("No subdomains found.")
            print("No subdomains found.")

    def get_cms_info(self):
        # Detect the Content Management System (CMS) used by the domain using BuiltWith
        self.log("Detecting CMS...")
        print("Detecting CMS...")
        try:
            tech_info = builtwith.parse(self.start_urls[0])
            if tech_info:
                technologies = set()  # Use a set to avoid duplicates
                for tech, items in tech_info.items():
                    technologies.update(items)
                if technologies:
                    self.cms_info = ', '.join(technologies)
                    self.log(f"CMS Information: Detected technologies - {self.cms_info}")
                    print(f"CMS Information: Detected technologies - {self.cms_info}")
                else:
                    self.cms_info = "No CMS technologies detected."
                    self.log(self.cms_info)
                    print(self.cms_info)
            else:
                self.cms_info = "No CMS detected."
                self.log(self.cms_info)
                print(self.cms_info)
        except Exception as e:
            self.cms_info = f"Error detecting CMS: {e}"
            self.log(self.cms_info)
            print(self.cms_info)

    def get_whois_info(self):
        # Perform Whois lookup to get domain registration and hosting information using python-whois
        self.log("Performing Whois lookup...")
        print("Performing Whois lookup...")
        try:
            w = whois.whois(self.domain)
            if w:
                self.whois_info['registrar'] = w.registrar if w.registrar else 'N/A'
                self.whois_info['name_servers'] = ', '.join(w.name_servers) if w.name_servers else 'N/A'
                self.whois_info['creation_date'] = w.creation_date[0].strftime("%Y-%m-%d") if isinstance(w.creation_date, list) else (w.creation_date.strftime("%Y-%m-%d") if w.creation_date else 'N/A')

                whois_info_str = (
                    f"Whois Information:\n  Registrar: {self.whois_info['registrar']}\n  Name Servers: {self.whois_info['name_servers']}\n  Creation Date: {self.whois_info['creation_date']}"
                )
                self.log(whois_info_str)
                print(whois_info_str)
            else:
                self.log("No Whois information found.")
                print("No Whois information found.")
        except Exception as e:
            self.log(f"Error with Whois lookup: {e}")
            print(f"Error with Whois lookup: {e}")

    def print_final_summary(self):
        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time
        # Prepare summary data
        summary = [
            f"Total Pages Crawled: {self.page_count}",
            f"Time Taken for Crawling: {elapsed_time:.2f} seconds",
        ]
        if self.subdomains:
            summary.append(f"Subdomains Found: {', '.join(self.subdomains)}")
        else:
            summary.append("Subdomains Found: None")
        if self.whois_info:
            summary.append("Whois Information:")
            summary.append(f"  Registrar: {self.whois_info.get('registrar', 'N/A')}")
            summary.append(f"  Name Servers: {self.whois_info.get('name_servers', 'N/A')}")
            summary.append(f"  Creation Date: {self.whois_info.get('creation_date', 'N/A')}")
        else:
            summary.append("Whois Information: None")
        if hasattr(self, 'cms_info'):
            summary.append(f"CMS Information: {self.cms_info}")
        else:
            summary.append("CMS Information: Not available")

        # Print summary
        print("\nFinal Summary:")
        for line in summary:
            print(line)

        # Store summary for writing to CSV
        self.summary_data = [self.start_urls[0], '\n'.join(summary)]

    def write_summary_to_csv(self):
        # Write the final summary to a CSV file
        with open('crawl_summary.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.summary_data)

if __name__ == "__main__":
    # Read the start URLs from a CSV file
    with open('url_start.csv', 'r') as file:
        csv_reader = csv.reader(file)
        urls = [row[0] for row in csv_reader]

    # Configure and start the Scrapy crawler
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'LOG_LEVEL': 'INFO',
        'HTTPERROR_ALLOW_ALL': True,
        'DEPTH_LIMIT': 5  # Adjust depth if needed
    })

    # Start the crawling process for each URL
    for url in urls:
        process.crawl(SiteCrawler, start_url=url)
    process.start()
