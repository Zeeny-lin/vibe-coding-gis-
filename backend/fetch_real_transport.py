"""
Fetch Real Transport Data from OpenStreetMap (Overpass API)
"""
import requests
import json
import os
import time

# List of Overpass API mirrors
OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://z.overpass-api.de/api/interpreter",
]

def fetch_overpass_data(query):
    for url in OVERPASS_URLS:
        print(f"Sending query to Overpass API ({url})...")
        try:
            response = requests.post(url, data={'data': query}, timeout=90)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Overpass API Error ({url}): {e}")
            time.sleep(2)
    return None

def convert_to_geojson(osm_data):
    if not osm_data: return None
    
    features = []
    nodes = {n['id']: n for n in osm_data.get('elements', []) if n['type'] == 'node'}
    
    for el in osm_data.get('elements', []):
        if el['type'] == 'way':
            coords = []
            valid = True
            for nid in el.get('nodes', []):
                if nid in nodes:
                    n = nodes[nid]
                    coords.append([n['lon'], n['lat']])
                else:
                    # Incomplete way, can skip or use partial. Overpass usually returns all nodes if requested properly.
                    pass
            
            if len(coords) > 1:
                props = el.get('tags', {})
                props['id'] = el['id']
                props['type'] = 'transport' # Generic type for POI
                
                # Determine subtype better
                if 'railway' in props and props['railway'] in ['rail', 'highspeed', 'narrow_gauge']:
                    props['subtype'] = 'railway'
                    props['name'] = props.get('name', 'Unknown Railway')
                elif 'highway' in props:
                    props['subtype'] = 'highway'
                    props['name'] = props.get('name', props.get('ref', 'Unknown Road'))
                else:
                    props['subtype'] = 'road'
                    
                features.append({
                    "type": "Feature",
                    "properties": props,
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coords
                    }
                })
                
    return {
        "type": "FeatureCollection",
        "features": features
    }

def main():
    # Query for Putian Area Railways and Major Highways
    # Using a slightly strict timeout and recursion
    query = """
    [out:json][timeout:90];
    (
      way["railway"~"rail"](24.9, 118.4, 25.7, 119.7);
      way["highway"~"motorway|trunk"](24.9, 118.4, 25.7, 119.7);
    );
    out body;
    >;
    out skel qt;
    """
    
    data = fetch_overpass_data(query)
    if data:
        geojson = convert_to_geojson(data)
        
        # Save
        out_dir = os.path.join(os.path.dirname(__file__), 'app/data/poi')
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, 'transport_real.geojson'), 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)
        print(f"Saved Real Transport Data with {len(geojson['features'])} features.")
    else:
        print("Failed to fetch transport data from all mirrors.")

if __name__ == '__main__':
    main()
