import json
import pandas as pd
from datetime import datetime

def menu():
    # Print het welkomstbericht en de menu-opties
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

def main():
    # Roept het menu aan en vraagt de gebruiker om een keuze te maken
    menu()
    keuze = input("Wat wil jij doen? ").strip().lower()
    
    # Blijf in de lus totdat de gebruiker 's' kiest om te stoppen
    while keuze != "s":
        if keuze == "a":
            # Toon de huidige tijdloze lijst
            song_list = tijdloze_lijst()
            print(song_list)
        elif keuze == "b":
            # Toon de huidige tijdloze lijst, aflopend op plaats
            song_list = tijdloze_lijst()
            tijdloze_lijst_aflopend(song_list)
        elif keuze == "c":
            # Toon de songs van de tijdloze lijst van een ander jaartal
            year = input("\nVan welke jaar wil jij zien? :")
            print(toon_tijdloze_lijst_jaartal(year))
        elif keuze == "d":
            # Toon enkel de songs die gestegen zijn ten opzichte van vorig jaar
            result = songs_gestegen_tov_vorig_jaar()
            print(result)
        elif keuze == "e":
            # Geef een lijst van songs van een bepaalde artiest
            artist = input("\nVan welke artiest wil jij zien? :").strip().lower()
            list = toon_songs_van_artiest(artist)
            print(list)
        elif keuze == "f":
            # Geef een lijst van songs waar een bepaald woord in de lyrics staat
            lyric = input("\nVan welke woord wil jij zien? :").strip().lower()
            print(toon_songs_met_lyric(lyric))
        elif keuze == "g":
            # Toon de top 10 artiesten die het meest in de lijst voorkomen
            toon_top_10_artiesten()
        elif keuze == "h":
            # Toon de huidige en vorige posities van een bepaalde song
            song = input("\nVan welke song wil jij zien? :").strip().lower().capitalize()
            print(toon_bepalde_song(song))
        elif keuze == "i":
            # Toon de top 15 songs die het langst in de lijst hebben gestaan
            toon_songs_die_langst_in_lijst_staan()
        
        # Print een lege regel en toon het menu opnieuw
        print()
        menu()
        keuze = input("\nWat wil jij doen? ").strip().lower()

def json_lezen() -> dict:
    # Leest de JSON-bestand en retourneert de data als een dictionary
    with open("stubru.json", "r") as json_file:
        data = json.load(json_file)
    return data

def tijdloze_lijst() -> pd.DataFrame:
    # Haalt de tijdloze lijst op en retourneert deze als een DataFrame
    song_list = json_lezen()
    song_list_dict = [
        {"position": song["position"], "previous": song["previous"], "verschil": song["previous"] - song["position"],
         "title": song["title"], "name": song["name"]} for song in song_list["songs"]]
    song_list_dict = pd.DataFrame(song_list_dict)
    return song_list_dict

def tijdloze_lijst_aflopend(song_list: pd.DataFrame) -> None:
    # Sorteert de tijdloze lijst aflopend op positie en print deze
    song_list_aflopend = song_list.sort_values(by=["position"], ascending=False)
    print(song_list_aflopend)

def toon_tijdloze_lijst_jaartal(year: str) -> pd.DataFrame:
    # Filtert de tijdloze lijst op een bepaald jaar en retourneert deze als een DataFrame
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

def songs_gestegen_tov_vorig_jaar() -> pd.DataFrame:
    # Haalt de songs op die gestegen zijn ten opzichte van vorig jaar en retourneert deze als een DataFrame
    song_list = json_lezen()
    song_list_dict = [
        {"position": song["position"], "previous": song["previous"], "verschil": song["previous"] - song["position"],
         "title": song["title"], "name": song["name"]} for song in song_list["songs"] if song["previous"] > song["position"]]
    song_list_dict = pd.DataFrame(song_list_dict)
    return song_list_dict

def toon_songs_van_artiest(artist: str) -> pd.DataFrame:
    # Haalt de songs op van een bepaalde artiest en retourneert deze als een DataFrame
    song_list = json_lezen()
    song_list_dict = [
        {"position": song["position"], "previous": song["previous"], "verschil": song["previous"] - song["position"],
         "title": song["title"], "name": song["name"]} for song in song_list["songs"] if artist in song["name"].lower()]
    song_list_dict = pd.DataFrame(song_list_dict)
    return song_list_dict

def toon_songs_met_lyric(lyric: str) -> pd.DataFrame:
    # Haalt de songs op waar een bepaald woord in de lyrics staat en retourneert deze als een DataFrame
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

def toon_top_10_artiesten() -> None:
    # Toont de top 10 artiesten die het meest in de lijst voorkomen
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

def toon_bepalde_song(song_title: str) -> pd.DataFrame:
    # Haalt de huidige en vorige posities op van een bepaalde song en retourneert deze als een DataFrame
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

def toon_songs_die_langst_in_lijst_staan() -> None:
    # Toont de top 15 songs die het langst in de lijst hebben gestaan
    song_list = json_lezen()["songs"]
    song_list_dict = pd.DataFrame(song_list)
    song_list_die_langst_staan = song_list_dict.sort_values("created_at", ascending=0).head(15)
    print(song_list_die_langst_staan)

# Start het programma
main()