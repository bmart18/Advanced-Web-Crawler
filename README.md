
# Advanced Web Crawler

![License](https://img.shields.io/badge/license-MIT-green)  
![Python](https://img.shields.io/badge/python-3.8%2B-blue)  
![Scrapy](https://img.shields.io/badge/scrapy-2.x-orange)  
![Sublist3r](https://img.shields.io/badge/sublist3r-1.x-yellow)

An advanced web crawler designed to extract comprehensive information from websites. This program utilizes the **Scrapy** framework for crawling and integrates various tools for subdomain enumeration, CMS detection, and Whois lookups.

---

## 🚀 Features

- **Web Crawling**: Crawl pages from a given URL, follow internal links, and exclude external resources.
- **Subdomain Enumeration**: Identify subdomains using Sublist3r.
- **CMS Detection**: Use BuiltWith to detect the technologies used by a website.
- **Whois Lookup**: Gather domain registration and hosting information.
- **Summary Reports**: Generate comprehensive crawl summaries with key metrics.
- **CSV Export**: Save the final summary to a CSV file.

---

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)

---

## 🔧 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/advanced-web-crawler.git
   cd advanced-web-crawler
   ```

2. **Install Dependencies**:
   Use the `requirements.txt` file to install the necessary Python libraries.
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

1. **Prepare the Input File**:
   Create a `url_start.csv` file containing the URLs to be crawled. Example format:
   ```csv
   https://example.com
   https://another-example.com
   ```

2. **Run the Program**:
   ```bash
   python site_crawler.py
   ```

3. **View the Results**:
   - Crawl summaries are printed in the console.
   - Subdomains, CMS information, and Whois details are logged and saved in `crawl_summary.csv`.

---

## 🛠️ Requirements

- Python 3.8 or higher
- Scrapy
- Sublist3r
- Requests
- BuiltWith
- python-whois
- dnspython

Install dependencies using:
```bash
pip install Scrapy sublist3r requests builtwith python-whois dnspython
```

---

## 🖋️ Contributing

We welcome contributions to improve this program! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Commit your changes (`git commit -m 'Add a new feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Open a pull request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 💡 Acknowledgments

- [Scrapy](https://scrapy.org/): For the robust web crawling framework.
- [Sublist3r](https://github.com/aboul3la/Sublist3r): For subdomain enumeration.
- [BuiltWith](https://builtwith.com/): For CMS and technology detection.
- [python-whois](https://pypi.org/project/whois/): For domain registration lookup.

---

### 🗂️ Directory Structure

```plaintext
advanced-web-crawler/
├── site_crawler.py      # Main program file
├── requirements.txt     # Python dependencies
├── url_start.csv        # Input file with URLs
├── crawl_summary.csv    # Output file with summary data
└── README.md            # Project documentation
```

---

Thank you for using **Advanced Web Crawler**! Feel free to report issues or suggest improvements.

🎉 **Happy crawling!**
