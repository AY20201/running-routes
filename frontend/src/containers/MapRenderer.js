import React from 'react'
import { MapContainer, TileLayer } from 'react-leaflet';
import RoutePolyline from './RoutePolyline'
import LocationMarker from './LocationMarker'
import styles from '../styles.module.css'
import 'leaflet/dist/leaflet.css';

function RenderMap({ currentPosition, activePath, kilometers, markerCallback })
{
    return (
        <MapContainer className = {styles.map} center={currentPosition} zoom={15}>
            <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
            <LocationMarker currentPosition={currentPosition} markerCallback={markerCallback}/>
            <RoutePolyline path={activePath} kilometers={kilometers}/>
        </MapContainer>
    );
    //needs to be inside a function so I can use useMemo hook
}

export default RenderMap;