# SpotlightLibre
Lightweight fulltext search for Calibre on Mac.
============================================================

Spotlight-based Full Text Search Plugin for Mac
Created by soychicka (August 2019)
Hacked together with code from https://manual.calibre-ebook.com/creating_plugins.html and Recoll Fulltext Search

Tested on Calibre >= 3.41.3 (as tested, it may run on earlier versions.  Lemme know if it doesn't?)

Runs only on OS X systems (uses Spotlight, which is only available in OS X).

This plugin lets you run a full text search in Calibre that uses your Mac's pre-existing Spotlight index to look inside your documents, displaying matches for the currently-open library in calibre.

That means it doesn't waste any disk space for a second index of the same documents.



 

Install
==============================

Steps to get this plugin working:
1. install plugin
	a) download
	b) from the command line, run 
			calibre-customize -b /path/to/where/you/put/it
	c) launch Calibre.

		

2. add a column to store ids
2.a) Open Preferencies > add your own columns
2.b) create a new column with:
			Lookup name: cid
			Column heading: CID
			Column type: "Column built from other columns"
			Template: {id}   # include brackets
			Sort/Search column by: number




3.  Relaunch Calibre and 
	 	Use it
		
		To search:  Cmd-Shift-X



Known issues
==============================

Searches with lots of matches may cause errors - I designed this to find outliers, like documents in my library that contain tangential references to persons of interest.  
Workaround: don't use generic terms in search.



Troubleshooting
==============================

If your books that you know match aren't currently showing up, make sure they show up in a normal Spotlight search.  

	If books don't show up in Spotlight, make sure the directory is NOT included under System Preferences > Spotlight > Privacy.

		Still nothing?  Try adding the main directory containing your Calibre libraries to the Privacy list, then immediately remove the directory from the list.  That should rebuild the index for the relevant files.


	If books show up in Spotlight but not in the Calibre results, make sure you're in the correct library.  
		If not, switch libraries!

		Still not working? add an issue here https://github.com/soychicka/SpotlightLibre/issues





Changes since 1.0.0
==============================
1.0.1 
- firsties