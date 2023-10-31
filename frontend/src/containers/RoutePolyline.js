import React from "react";
import { Polyline, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function findEstimatedTime(paceInSeconds, distance)
{
    let totalTime = Math.floor(distance * paceInSeconds);
    let hours = Math.floor(totalTime / 3600);
    let minutes = Math.floor((totalTime - hours * 3600) / 60)
    let seconds = totalTime - hours * 3600 - minutes * 60;
    
    if(seconds < 10){
        seconds = `0${seconds}`
    }
    if(minutes < 10 && hours >= 1){
        minutes = `0${minutes}`
    }


    if(hours === 0) {
        return `${minutes}:${seconds}`;
    } else {
        return `${hours}:${minutes}:${seconds}`;
    }
}

function RoutePolyline({ path, kilometers })
{
    const map = useMap();
    const lineColor = { color: 'rgb(120, 73, 196)' };
    let dist = path.distance;
    //console.log(path.distance / path.path.length);

    let t1, t2, t3, t4 = "";
    if(kilometers){
        dist = dist * 1.609;
        t1 = `Time at 5:30/kilometer: ${findEstimatedTime(60 * 5.50, dist)}`;
        t2 = `Time at 5:00/kilometer: ${findEstimatedTime(60 * 5.00, dist)}`;
        t3 = `Time at 4:30/kilometer: ${findEstimatedTime(60 * 4.50, dist)}`;
        t4 = `Time at 4:00/kilometer: ${findEstimatedTime(60 * 4.00, dist)}`;
        //eg = `Elevation Gain: ${path.elevation_gain} meters`;
    } else {
        t1 = `Time at 9:00/mile: ${findEstimatedTime(60 * 9.00, dist)}`;
        t2 = `Time at 8:00/mile: ${findEstimatedTime(60 * 8.00, dist)}`;
        t3 = `Time at 7:00/mile: ${findEstimatedTime(60 * 7.00, dist)}`;
        t4 = `Time at 6:00/mile: ${findEstimatedTime(60 * 6.00, dist)}`;
        //eg = `Elevation Gain: ${Math.floor(path.elevation_gain * 3.28)} feet`;
    }

    if(path.path.length > 0)
    {
        map.setView(path.center, 15);
    }

    return(
        <Polyline pathOptions={lineColor} positions={path.path}>
            <Popup>
                {`Distance: ${Math.round(dist * 100.0) / 100.0} ${kilometers ? "kilometers" : "miles"}`}<br/>
                {t1}<br/>{t2}<br/>{t3}<br/>{t4}
            </Popup>
        </Polyline>
    );
}

export default React.memo(RoutePolyline);