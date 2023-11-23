# Project Setup and Execution Guide

## Project Description
<p>This project utilizes the Scrapy framework to scrape the first 500 items (title, address, price, and image URL) from sreality.cz (flats for sale) and saves the data in a PostgreSQL database. Additionally, it implements a simple HTTP server in Python using the Asyncio and FastAPI frameworks to display the scraped ads on <a href="http://127.0.0.1:8080" target="_new">http://127.0.0.1:8080</a>.</p>

### Project Structure
<ul>
<li><strong>requirements.in</strong>: Contains dependencies and required Python 3.11 libraries.</li>
<li><strong>migrate.py</strong>: Logic to create a database and tables for saving ads, along with required indexes.</li>
<li><strong>scraper.py</strong>: Scrapes <a href="https://www.sreality.cz/en/search/for-sale/apartments" target="_new">https://www.sreality.cz/en/search/for-sale/apartments</a> using the Scrapy framework. Saves data to PostgreSQL using SQLAlchemy ORM. Supports command-line execution with arguments.</li>
<li><strong>app.py</strong>: Main logic for displaying scraped ads on <a href="http://127.0.0.1:8080" target="_new">http://127.0.0.1:8080</a> using Asyncio and FastAPI. Connects to PostgreSQL using environment variables.</li>
<li><strong>docker-compose.yaml</strong>: Orchestrates containers for Postgres, database setup, , Selenium WebDriver, scraper, and app. Ensures container dependencies are met.</li></ul>


### HTML Structure

<p>The HTML structure of the ads is based on DIV elements with a specific order attribute. Relevant data such as title, address, price, and image URL can be extracted from the structure.</p>

<p><strong>Example Structure:</strong></p>

<pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 gizmo:dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>html</span></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-html"><span class="hljs-tag">&lt;<span class="hljs-name">div</span> <span class="hljs-attr">style</span>=<span class="hljs-string">"order: 0;"</span>&gt;</span>
    <span class="hljs-tag">&lt;<span class="hljs-name">a</span> <span class="hljs-attr">href</span>=<span class="hljs-string">"/en/detail/sale/flat/4+kt/praha-praha-2-/586169180"</span> <span class="hljs-attr">class</span>=<span class="hljs-string">"title"</span>&gt;</span>
        <span class="hljs-tag">&lt;<span class="hljs-name">span</span> <span class="hljs-attr">class</span>=<span class="hljs-string">"name ng-binding"</span>&gt;</span>For sale apartment 4+kt 140<span class="hljs-symbol">&amp;nbsp;</span>m²<span class="hljs-tag">&lt;/<span class="hljs-name">span</span>&gt;</span>
    <span class="hljs-tag">&lt;/<span class="hljs-name">a</span>&gt;</span>
    <span class="hljs-tag">&lt;<span class="hljs-name">span</span> <span class="hljs-attr">class</span>=<span class="hljs-string">"locality ng-binding"</span>&gt;</span>Praha 2<span class="hljs-tag">&lt;/<span class="hljs-name">span</span>&gt;</span>
    <span class="hljs-tag">&lt;<span class="hljs-name">span</span> <span class="hljs-attr">class</span>=<span class="hljs-string">"norm-price ng-binding"</span>&gt;</span>Information about price at agency<span class="hljs-tag">&lt;/<span class="hljs-name">span</span>&gt;</span>
    <span class="hljs-tag">&lt;<span class="hljs-name">a</span> <span class="hljs-attr">href</span>=<span class="hljs-string">"/en/detail/sale/flat/4+kt/praha-praha-2-/586169180"</span> <span class="hljs-attr">class</span>=<span class="hljs-string">"_2vc3VMce92XEJFrv8_jaeN"</span> <span class="hljs-attr">tabindex</span>=<span class="hljs-string">"-1"</span> <span class="hljs-attr">rel</span>=<span class="hljs-string">"nofollow"</span>&gt;</span>
        <span class="hljs-tag">&lt;<span class="hljs-name">img</span> <span class="hljs-attr">src</span>=<span class="hljs-string">"https://d18-a.sdn.cz/d_18/c_img_QI_JV/qs5SAt.jpeg?fl=res,400,300,3|shr,,20|jpg,90"</span> <span class="hljs-attr">alt</span>=<span class="hljs-string">""</span>&gt;</span>
    <span class="hljs-tag">&lt;/<span class="hljs-name">a</span>&gt;</span>
<span class="hljs-tag">&lt;/<span class="hljs-name">div</span>&gt;</span>
</code></div></div></pre>

### Environment Variables
<ul>
<li>POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PSWD, POSTGRES_DB: Connection details for PostgreSQL.</li>
<li>WEBDRIVER_HOST, WEBDRIVER_PORT: Connection details for Selenium WebDriver.</li>
<li>APP_PORT: Application port</li>
</ul>

### Docker Compose
<ul><li>Defines containers for Postgres, database setup, Selenium WebDriver, scraper, and app.</li><li>Ensures container dependencies are satisfied.</li></ul>


## Usage
<ul>
<li>Run the provided commands for local development or use <code>docker-compose up</code> for Docker execution.</li>
<li>Access the scraped ads on <a href="http://127.0.0.1:8080" target="_new">http://127.0.0.1:8080</a> after starting the app.</li>
</ul>

<p><strong>Note:</strong> Ensure proper environment variables are set before running the application. Adjustments may be needed based on specific system configurations.</p>

## Local Development

### Prerequisites
<ul><li>Python 3.11</li><li>Docker</li></ul>

### Create Virtual Environment

```
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment on Linux or macOS
source .venv/bin/activate

# Activate the virtual environment on Windows
.\.venv\Scripts\activate
```
### Install Dependencies

```
# Upgrade pip
pip install --upgrade pip

# Install pip-tools
pip install pip-tools

# Generate requirements.txt
pip-compile requirements.in

# Install dependencies
pip install -r requirements.txt
```

### Docker Compose - Start Containers

```
# Start containers with Postgres and Selenium WebDriver
docker-compose up postgres selenium
```

### Set Environment Variables

```
# Set environment variables (example)
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=luxonis
export POSTGRES_PSWD=luxonis
export POSTGRES_DB=sreality
export WEBDRIVER_HOST=localhost
export WEBDRIVER_PORT=4444
export APP_PORT=8080
```

### Run Migration Script

```
# Run migration script
python src/migration.py
```

### Run Scraper

```
# Run scraper
python src/scraper.py --spider=sreality --base-url=https://www.sreality.cz --path=/en/search/for-sale/apartments --pages=25
```

### Start the App

```
# Start the app
python src/app.py
```


## Docker Setup and Execution
### Prerequisites
<ul><li>Docker</li><li>Docker Compose</li></ul>

### Start Containers

```
# Start all containers
docker-compose up
```
