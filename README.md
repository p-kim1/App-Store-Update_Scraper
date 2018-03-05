# App-Store-Update-Scraper
A Python script that obtains HTML data from the iOS App Store and scrapes the most recent updates of a given app.

**Features:**  
* Data Type Selection: Specify an app to analyze, or choose from 3 categories in the Top 100 apps section (Free, Paid, or Top-Grossing).
* Generate Datasets: Save the update data as either a .txt or .csv file.
* Generate Timeline Plots:  Generate and save update timeline plots for a specified app.
* Print Updates: Print update data to the terminal, formatted in columns for version number and release date.  

**Planned Changes/Features:**  
* Google Play Store version  
* Additional graphs types and statistics  
* Graph generation for Top 100 data  
* Obtaining and generating statistics for app reviews  
* Compatibility with non-Linux operating systems  

**Modules:**  
* Beautiful Soup  
* Matplotlib  
* Google Search API (provided)  
* datetime  
* urllib  
* sys  
* os  
  
**Run on command line with:** python3 htmlScraper.py
