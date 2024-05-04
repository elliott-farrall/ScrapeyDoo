# ScrapeyDoo

ScrapeyDoo is a web scraping application designed to gather data from Amazon book listings.

## Installation

To install ScrapeyDoo, download the latest executable from the [Releases](https://github.com/ElliottSullingeFarrall/ScrapeyDoo/releases) page.

## Usage

After running ScrapeyDoo, the scraped data will be stored in a folder named `scraps` located in the same directory as the executable. The data is stored in CSV format in a file named `scrap.csv` under a directory named with the timestamp of the scrape.

## Development

ScrapeyDoo comes with a development environment configured using Nix Flakes and Poetry. 

For non-Nix users, a Nix devcontainer is also included. 

To set up the development environment, follow these steps:

1. Clone the repository: `git clone https://github.com/ElliottSullingeFarrall/ScrapeyDoo.git`
2. Navigate into the project directory: `cd ScrapeyDoo`
3. Run `nix develop` to enter the development environment.
