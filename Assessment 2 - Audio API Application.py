import tkinter as tk
from tkinter import ttk
import requests
import pandas as pd
import webbrowser

"""Youtube MV Jukebox Application"""

#This section focuses on getting the video data from the API.
def Video_Data (artist_name):
    Search_url = f"https://www.theaudiodb.com/api/v1/json/123/search.php?s={artist_name}"

    try:
        search_res = requests.get(Search_url).json()
        artist_id = search_res ['artists'][0]['idArtist']

        Video_url = f"https://www.theaudiodb.com/api/v1/json/123/mvid.php?i={artist_id}"
        Video_res = requests.get(Video_url).json()
        return pd.DataFrame(Video_res['mvids']) #pandas is used to easily get the data from the API and organize them without coding.
    except:
        return None
    
#This section is the main application GUI.

class JukeboxMV:
    # This allows the application to load the list of artist along with their videos, music tracks and albums.
    # And it searches if that artist has a music video or not.
    def Load_List (MV_App):
        MV_App.listbox.delete (0, tk.END)
        Artist = MV_App.Entry.get()
        dataframe = Video_Data(Artist)

        if dataframe is not None:
            MV_App.Video_Data_Storage = dataframe
            for index, row in dataframe.iterrows():
                # Added a safety check (.get) so it doesn't crash if 'strAlbum' is missing
                track = row.get('strTrack', 'Unknown Track')
                album = row.get('strAlbum', 'No Album')
                MV_App.listbox.insert(tk.END, f"{track}, ({album})")    
        else:
            MV_App.listbox.insert(tk.END, "No MVs found for this artist.")

    def Play_Video(MV_App):
        Selection = MV_App.listbox.curselection()
        if Selection and MV_App.Video_Data_Storage is not None:
            index = Selection [0]
            MV_Video_url = MV_App.Video_Data_Storage.iloc[index]['strMusicVid']
            if MV_Video_url:
                webbrowser.open(MV_Video_url)

    def __init__(MV_App,Root):
        MV_App.Root = Root
        MV_App.Root.title("MV Jukebox")
        MV_App.Root.geometry ("800x600")

        tk.Label(Root, text="Artist MV Jukebox", font=("Monoid", 16, "bold")).pack(pady=10)

        #The search box for the artist.
        MV_App.Entry = tk.Entry (Root, font=("Monoid", 12))
        MV_App.Entry.insert(0, "Coldplay")
        MV_App.Entry.pack(pady=5)

        MV_App.Btn = ttk.Button(Root, text = "Load Videos", command=MV_App.Load_List) #This loads the list of music videos from the artist.
        MV_App.Btn.pack(pady = 10, padx = 10)

        MV_App.listbox = tk.Listbox(Root, width = 70, height = 15)
        MV_App.listbox.pack(pady = 10, padx = 10)

        MV_App.Play_Btn = ttk.Button (Root, text = " Play Video", command=MV_App.Play_Video) #This allows the video to be played when the button is pressed.
        MV_App.Play_Btn.pack(pady = 5)

        MV_App.Video_Data_Storage = None

if __name__ == "__main__":
    Root = tk.Tk()
    Audio_API_App = JukeboxMV(Root)
    Root.mainloop()