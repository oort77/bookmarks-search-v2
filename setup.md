**Setup and configuration**

1.	Install all Python packages from requrements.txt
2.	Create PostgreSQL database
3.	Open file .streamlit/secrets.toml in project folder:  
	- fill PostgreSQL connection credentials in the ["postgres"] section  
	- edit the ["bookmarks_path"] section with the path to your Chrome
	  browser bookmarks

**Operation**

In your Terminal cd to project folder and type

	streamlit run st_psql.py &

The search page opens in your browser.

Check "Full update" box in the left bottom part of the page and
press "Update" button. Search database generation may take a while.

You may choose to do partial updates from time to time: press
"Update" button with clear "Full update" box. Partial updates are 
much faster, as only the new bookmarks are scraped.

Checked with python versions 3.8 and 3.9.
