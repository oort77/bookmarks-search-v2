# Brave search
**Search Chrome/Brave bookmarked sites' content -- PostgreSQL backend**   

Brave search solves the problem of finding relevant content in your bowser's bookmarks, and works with Chrome and Brave browsers.   
   
**Configuration and setup**    

The system requres a PostgreSQL database engine to be installed and configured. Path to your browser's bookmarks file has to be specified as well in ```.streamlit/secrets.toml```. Refer to ```setup.md```

If you wish to block certain sites from being parsed, include them in ```black_list.toml```.

**Running Brave search**

Type

    ```cd path_to_brave_search_folder && streamlit run st_psql.py --server.port 9500 &```   
    
The command will open a browser tab with a search prompt. Google-style queries are supported.   

You can specify the number of results on screen, as well as number of characters shown for each of them.   

Search can be "limited" to Russian, although the engine recognizes the language of a search request automatically.

**Updating database**

Database must be updated manually. Widget ```Keep it fresh``` is located in the lower part of the left pane.
Both partial and full updates are supported. Please note that update may take a while if you have many bookmarks.

**Working environment**

The system has been tested on Mac OS 10.14.6, Python 3.8 with PostgreSQL server 12.11 running on Ubuntu 22.04. 
PostgreSQL can rbe installed and run on the same compyter, there is no need for a separate dedicated server.

The only Mac specific feature is voice notifications, can be commented out.

   
<img width="1570" alt="Brave search screenshot" src="https://user-images.githubusercontent.com/73858914/171838393-b2409d53-367e-410b-a6c7-bc2db3db86c6.png">
