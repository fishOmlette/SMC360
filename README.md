# SMC360 — Social Media Data Connector

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

**SMC360** is a unified toolkit for extracting, parsing, and managing social media data at scale.  
It provides both a **command-line interface (CLI)** and a **web interface**, enabling flexible integration into automated workflows and user-friendly interactive environments.

---

## ✨ Features

- **Multi-Platform Support**
  - YouTube (YouTube Data API)  
  - Instagram (Basic Display API)  

- **Data Persistence**
  - Databases: PostgreSQL, Snowflake  
  - Object Storage: Amazon S3  

- **Flexible Interfaces**
  - **CLI Tool** — for automation, scheduling, and scripting  
  - **Web Interface** — for interactive extraction and monitoring  

- **Dual Storage**
  - **Parsed Data** → relational databases for analytics  
  - **Raw API Responses** → object storage for traceability and reprocessing  

---

## 🚀 Installation

```bash
pip install "git+https://github.com/Mdadilfarooq/social_media_connector.git@main"
````

---

## ⚡ Quickstart

### 1. Configure

Prepare a configuration file (`config.yaml`) with your API keys, database credentials, and storage settings:

```yaml
platform:
  name: youtube
  api_key: YOUR_YOUTUBE_API_KEY

database:
  type: postgresql
  host: localhost
  port: 5432
  user: postgres
  password: secret
  database: SMC360

storage:
  type: s3
  bucket: SMC360-data
  access_key: YOUR_AWS_KEY
  secret_key: YOUR_AWS_SECRET
```

---

### 2. CLI Usage

Extract and store social media data directly from the terminal:

```bash
SMC360 extract --config config.yaml --platform youtube
```

Other commands:

```bash
SMC360 extract --platform instagram
SMC360 status
SMC360 config validate
```

---

### 3. Web Interface

Launch the web app for interactive control:

```bash
SMC360 web
```

Open [http://localhost:8000](http://localhost:8000) to manage configurations, run extractions, and monitor jobs.

---

## 📂 Workflow

1. **Configuration** — Connect to the chosen social media platform, database, and storage service.
2. **Dynamic Loading** — Pull additional configuration from object storage.
3. **Extraction & Parsing** — Collect raw data via APIs and convert it into structured formats.
4. **Storage** — Save structured data into databases and archive raw responses in object storage.

---

## 💡 Use Cases

* Social media analytics and insights
* Data warehousing for BI/reporting
* Marketing and campaign performance tracking
* Archival of raw API responses for compliance and auditing

---

## 🛠 Development

Clone the repo and install in editable mode:

```bash
git clone https://github.com/Mdadilfarooq/social_media_connector.git
cd social_media_connector
pip install -e .
```

Run tests:

```bash
pytest
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

