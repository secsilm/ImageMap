# coding: utf-8

import json
import os
from locate import locate
import fire


def get_points(in_dir):
    '''Get points latlngs'''
    points = []
    file_format = ['jpg', 'jpeg', 'png']
    if os.path.isdir(in_dir):
        files = os.scandir(in_dir)
        for file in files:
            if file.name.split('.')[-1] in file_format and file.is_file():
                # Include address infomation and latlng
                address = locate(file.path)
                if address:
                    lat, lng = address.google_latlng.split(',')
                    points.append((float(lat), float(lng)))
    return points


class ImageMap(object):

    def __init__(self, points, style='night', out_dir=None):
        '''Initialize some parameters.
           poinst: list of tuples, (lat, lng).
           style: Google map style name which is in styles.json file.
           You can add your style or change it.
           out_dir: the path of html file'''
        try:
            with open('styles.json', 'r') as f:
                styles = json.load(f)
        except FileNotFoundError:
            print('File styles.json not found!')
        self.points = points
        self.style = styles[style]
        self.out_dir = out_dir

    def generate_html(self):
        '''Generate the html file'''
        try:
            center_lat = sum([p[0] for p in self.points]) / len(self.points)
            center_lng = sum([p[1] for p in self.points]) / len(self.points)
        except ZeroDivisionError:
            print('No points! Please add some points. Your images may have no GPS info.')
        locations = []
        for point in self.points:
            locations.append({'lat': point[0], 'lng': point[1]})
        locations = 'var locations = ' + json.dumps(locations).replace('"', '')
        html_code = '''
            <!DOCTYPE html>
            <html>
              <head>
                <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
                <meta charset="utf-8">
                <title>Marker Clustering</title>
                <style>
                  /* Always set the map height explicitly to define the size of the div
                  * element that contains the map. */
                  #map {{
                    height: 100%;
                  }}
                  /* Optional: Makes the sample page fill the window. */
                  html, body {{
                    height: 100%;
                    margin: 0;
                    padding: 0;
                  }}
                </style>
              </head>
              <body>
                <div id="map"></div>
                <script>

                  function initMap() {{

                    var map = new google.maps.Map(document.getElementById('map'), {{
                      zoom: 5,
                      center: {{lat: {center_lat}, lng: {center_lng}}},
                      styles: {style}
                    }});

                    // Create an array of alphabetical characters used to label the markers.
                    var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

                    // Add some markers to the map.
                    // Note: The code uses the JavaScript Array.prototype.map() method to
                    // create an array of markers based on a given "locations" array.
                    // The map() method here has nothing to do with the Google Maps API.
                    var markers = locations.map(function(location, i) {{
                      return new google.maps.Marker({{
                        position: location,
                        label: labels[i % labels.length]
                      }});
                    }});

                    // Add a marker clusterer to manage the markers.
                    var markerCluster = new MarkerClusterer(map, markers,
                        {{imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'}});
                  }}
                  {locations}
                </script>
                <script src="https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/markerclusterer.js">
                </script>
                <script async defer
                src="https://maps.googleapis.com/maps/api/js?callback=initMap">
                </script>
              </body>
            </html>'''
        html = html_code.format(
            center_lat=center_lat,
            center_lng=center_lng,
            locations=locations,
            style=self.style)
        if self.out_dir:
            with open(os.path.join(self.out_dir, 'output.html'), 'w') as f:
                print(html, file=f)
        else:
            with open('output.html', 'w') as f:
                print(html, file=f)


def main(in_dir, out_dir=None, style='night'):
    points = get_points(in_dir)
    m = ImageMap(points=points, style=style, out_dir=out_dir)
    m.generate_html()

if __name__ == '__main__':
    fire.Fire(main)
