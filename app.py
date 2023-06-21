import pandas as pd
from flask import Flask
import folium
from folium import plugins


app = Flask(__name__)
df = pd.read_csv('data.csv', encoding='big5', engine='pyarrow')
districts = df['行政區'].drop_duplicates()

records = []
for row in df.itertuples(index=False, name=None):
    try:
        record = {
            'district': row[0],
            'road': row[1],
            'others': row[2],
            'longitude': float(row[3]),
            'latitude': float(row[4])
        }
        records.append(record)
    except Exception as e:
        print('record: ', record, ', error: ', e)
# print(records)


@app.route('/')
def index():
    m = folium.Map(location=[25, 121.5], zoom_start=11, prefer_canvas=True)

    # Create a marker cluster dictionary to store marker clusters for each district
    marker_cluster = {}
    for district in districts:
        # Create a feature group for each district and add it to the map
        district_layer = folium.FeatureGroup(
            name=district, show=True).add_to(m)
        marker_cluster[district] = plugins.MarkerCluster().add_to(
            district_layer)

    # Add markers to the corresponding marker clusters based on the district
    for record in records:
        html = f'''
        <table class="table">
          <tbody>
            <tr>
              <th scope="row">行政區</th>
              <td>{record['district']}</td>
            </tr>
            <tr>
              <th scope="row">地址</th>
              <td>{record['others']}</td>
            </tr>
            <tr>
              <th scope="row">緯度</th>
              <td>{record['latitude']}</td>
            </tr>
            <tr>
              <th scope="row">經度</th>
              <td>{record['longitude']}</td>
            </tr>
          </tbody>
        </table>
        <a type="button" class="btn btn-light" href="https://www.google.com/maps/search/?api=1&query={record['latitude']},{record['longitude']}" target="_blank">Google Map</a>
        '''
        popup = folium.Popup(html, max_width=500, lazy=True)
        folium.Marker([record['latitude'], record['longitude']],
                      popup=popup).add_to(marker_cluster[record['district']])

    # Add a layer control to the map
    folium.LayerControl(collapsed=False).add_to(m)

    # Return the rendered HTML of the map
    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
