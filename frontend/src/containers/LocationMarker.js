import React, { useState } from "react";
import { Marker, Popup, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
    iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
    iconUrl: require('leaflet/dist/images/marker-icon.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

function LocationMarker( { currentPosition, markerCallback } ) {
    
    const [position, setPosition] = useState(currentPosition)
    const [cursorPosition, setCursorPosition] = useState(null);
    
    const map = useMapEvents({
        mousemove(e) {
            setCursorPosition(e.latlng);
        },
        click: () => {
            setPosition(cursorPosition);
            markerCallback(cursorPosition);
        },
    })
    
    return (
        <div>
        <Marker position={ position }>
            <Popup>
                The route's starting and ending point
            </Popup>
        </Marker>
        </div>
    )
}

export default LocationMarker;