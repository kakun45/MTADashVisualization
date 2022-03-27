import folium
import pandas

# import branca.colormap as cm

data = pandas.read_csv("merged_left_whole_city_final_whole.csv")

lat = list(data["LAT"])
lon = list(data["LON"])
exits = list(data["EXITS_diff_sum"])
entries = list(data["ENTRIES_diff_sum"])
station = list(data["station_id"])


def color_producer_ex(exits):
    if exits < 3000:
        return "beige"
    elif 3000 <= exits < 10000:
        return "orange"
    else:
        return "pink"


map = folium.Map(location=[40.762796, -73.967686], zoom_start=14, tiles="Stamen Toner")

fgv = folium.FeatureGroup(name="MTA_Exits")

for lt, ln, ex, st in zip(lat, lon, exits, station):
    fgv.add_child(
        folium.CircleMarker(
            location=[lt, ln],
            radius=ex / 10000,
            popup=str(ex) + " ppl Exit @ " + (st),
            fill_color=color_producer_ex(ex),
            fill=False,
            color="red",
            fill_opacity=0.1,
        )
    )

fgp = folium.FeatureGroup(name="MTA_Entries")


def color_producer_ent(entries):
    if entries < 3000:
        return "lightgreen"
    elif 3000 <= entries < 10000:
        return "yellow"
    else:
        return "darkgreen"


for lt, ln, en, st in zip(lat, lon, entries, station):
    fgp.add_child(
        folium.CircleMarker(
            location=[lt, ln],
            radius=en / 10000,
            popup=str(en) + " ppl Enter @" + (st),
            fill_color=color_producer_ent(en),
            fill=False,
            color="green",
            fill_opacity=0.1,
        )
    )

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save("Map4.html")
