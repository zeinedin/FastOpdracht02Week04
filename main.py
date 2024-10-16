import json
import pandas as pd
from datetime import datetime


def main():
    print("Welkom bij de Tijdloze lijst, wat wil je doen.")
    print("A) Toon huidige tijdloze lijst (Plaats/vorige plaats/verschil/titel/artiest)")
    print("B) Toon huidige tijdloze lijst (Aflopend op plaats)")
    print("C) Toon de songs van de tijdloze lijst van een ander jaartal")
    print("D) Toon enkel de songs die gestegen zijn ten opzichte van vorig jaar.")
    print("E) Geef een lijst van song(s) van een bepaalde artiest")
    print("F) Geef een lijst van song(s) waar volgend woord in de lyrics staat")
    print("G) Toon de top 10 artiesten die het meest in de lijst voorkomen.")
    print("H) Toon de huidige (en de vorige) posities van één bepaalde song.")
    print("I) Toon de top 15 songs die het langs in de lijst hebben gestaan.")
    print("S) (Stop)")
    keuze = input("Wat wil jij doen? ").strip().lower()

    while keuze != "s":
        if keuze == "a":
            song_list = tijdloze_lijst()
            print(song_list)
        elif keuze == "b":
            song_list = tijdloze_lijst()
            tijdloze_lijst_aflopend(song_list)
        elif keuze == "c":
            year = input("\nVan welke jaar wil jij zien? :")
            print(toon_tijdloze_lijst_jaartal(year))
        elif keuze == "d":
            result = songs_gestegen_tov_vorig_jaar()
            print(result)
        elif keuze == "e":
            artist = input("\nVan welke artiest wil jij zien? :").strip().lower()
            print(toon_songs_van_artiest(artist))
        elif keuze == "f":
            lyric = input("\nVan welke woord wil jij zien? :").strip().lower()
            print(toon_songs_met_lyric(lyric))
        elif keuze == "g":
            toon_top_10_artiesten()
        elif keuze == "h":
            song = input("\nVan welke song wil jij zien? :").strip().lower().capitalize()
            print(toon_bepalde_song(song))
        elif keuze == "i":
            toon_songs_die_langst_in_lijst_staan()
        keuze = input("\nWat wil jij doen? ").strip().lower()

def json_lezen():
    with open("stubru.json", "r") as json_file:
        data = json.load(json_file)

    return data
def tijdloze_lijst():
    song_list = json_lezen()
    song_list_dict = [
        {"position": song["position"], "previous": song["previous"], "verschil": song["previous"] - song["position"],
         "title": song["title"], "name": song["name"]} for song in song_list["songs"]]
    song_list_dict = pd.DataFrame(song_list_dict)
    return song_list_dict

    pass
def tijdloze_lijst_aflopend(song_list: [list]):
    song_list_aflopend = song_list.sort_values(by=["position"], ascending=False)
    print(song_list_aflopend)
def toon_tijdloze_lijst_jaartal(year: str):
    song_list = json_lezen()["songs"]
    song_list_year_filtered = []
    for song in song_list:
        list_year = str(datetime.fromtimestamp(int(song["modified_at"])))[0:4]
        if list_year == year:
            new_song = {
                "position": song["position"],
                "previous": song["previous"],
                "verschil": song["previous"] - song["position"],
                "title": song["title"],
                "name": song["name"],
            }
            song_list_year_filtered.append(new_song)
    return pd.DataFrame(song_list_year_filtered)
def songs_gestegen_tov_vorig_jaar():
    song_list = json_lezen()
    song_list_dict = [
        {"position": song["position"], "previous": song["previous"], "verschil": song["previous"] - song["position"],
         "title": song["title"], "name": song["name"]} for song in song_list["songs"] if song["previous"] > song["position"]]
    song_list_dict = pd.DataFrame(song_list_dict)
    return song_list_dict
def toon_songs_van_artiest(artist : str):
    song_list = json_lezen()
    song_list_dict = [
        {"position": song["position"], "previous": song["previous"], "verschil": song["previous"] - song["position"],
         "title": song["title"], "name": song["name"]} for song in song_list["songs"] if artist in song["name"].lower()]
    song_list_dict = pd.DataFrame(song_list_dict)
    return song_list_dict
def toon_songs_met_lyric(lyric: str):
    song_list = json_lezen()["songs"]
    song_list_lyric_filtered = []
    for song in song_list:
        song_lyric = song["lyrics"]
        if song_lyric and lyric in song_lyric:
            new_song = {
                "position": song["position"],
                "previous": song["previous"],
                "verschil": song["previous"] - song["position"],
                "title": song["title"],
                "name": song["name"],
            }
            song_list_lyric_filtered.append(new_song)
    return pd.DataFrame(song_list_lyric_filtered)
def toon_top_10_artiesten():
    song_list = json_lezen()["songs"]
    song_artists = [song["main_artist"] for song in song_list]
    song_artist_series = pd.Series(song_artists)
    song_artist_counts = song_artist_series.value_counts().head(10)
    main_artists = [artist for artist in song_artist_counts.index]
    song_list_top_filtered = []
    for song in song_list:
        if song["main_artist"] in main_artists:
            if song["name"] not in song_list_top_filtered:
                song_list_top_filtered.append(song["name"])
    song_list_dict = pd.DataFrame(song_list_top_filtered)
    song_list_dict = song_list_dict.rename(columns={0: "Artist Name"})
    print(song_list_dict)
def toon_bepalde_song(song_title: str):
    song_list = json_lezen()["songs"]
    song_list_lyric_filtered = []
    for song in song_list:
        if song["title"] == song_title:
            new_song = {
                "position": song["position"],
                "previous": song["previous"],
                "verschil": song["previous"] - song["position"],
                "title": song["title"],
                "name": song["name"],
            }
            song_list_lyric_filtered.append(new_song)
    return pd.DataFrame(song_list_lyric_filtered)
def toon_songs_die_langst_in_lijst_staan():
    song_list = json_lezen()["songs"]
    song_artists = [song["main_artist"] for song in song_list]
    song_artist_series = pd.Series(song_artists)
    song_artist_counts = song_artist_series.value_counts().head(10)
    print(song_artist_counts)
main()