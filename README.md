# YT-coPYcat
A fun tool to find Youtube Channels

# Instructions: 
• Make sure the Python Google API Client is installed:<br>
```-pip install google-api-python-client```<br>
• Enter your Youtube API V3 Key<br>
• Enter channel name<br>
• Enter desired number of returned channels<br>

# Editing Functions
To edit the amount of letters that are changed in each search, edit the ```max_typos=0``` variable in
```def generate_variants(name, max_typos=0):```<br><br>

Additionally, the replaced letters can be edited as well by changing the lists in ```LETTER_REPLACEMENTS```<br>
The current replacements are all adjacent keys and numerical replacements.
