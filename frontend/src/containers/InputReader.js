import React, { Component } from "react";
import MapRenderer from './MapRenderer'
import styles from '../styles.module.css'
import 'leaflet/dist/leaflet.css'
import titleImg from '../running_man_text.png'

class InputReader extends Component {
    
    state = 
    {
        data: {},
        textBoxValues: {},
        currentPosition: {},
        usedPosition: {},
        displayedPathIndex: -1,
        kilometers: 0,
        loading: false,
        requestError: "",
        pathsExist: false
    }

    markerCallback = (position) => {
        let roundedPosition = {lat: position.lat, lng: position.lng};
        this.setState({usedPosition: roundedPosition});
    }

    handleInputChange = (e, key) => {
        let copyParams = { ...this.state.textBoxValues, [key]: e.target.value};
        this.setState({textBoxValues: copyParams});

        if(this.state.currentPosition.lat === undefined) //assumes you won't change loc before reloading page
        {
            if(navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(this.success, this.error);
            } else {
                console.log("Could not use geolocation");
                this.setState({currentPosition: {lat:51.505, lng:-0.09}});
            }
        }
    }

    handleSubmit = () =>
    {
        if(this.state.usedPosition.lat === undefined || this.state.usedPosition.lng === undefined) {
            this.setState({usedPosition: this.state.currentPosition}, () => {
                this.getLoops()
            });
        } else {
            this.getLoops();
        }

        console.log("Button Pressed");
    }

    cyclePaths = (change, random) =>
    {
        if(this.state.pathsExist) {
            if(random) {
                let rand_index = Math.floor(Math.random() * (this.state.data.loops.length - 1));
                while(rand_index === this.state.displayedPathIndex && this.state.data.loops.length > 1) {
                    rand_index = Math.floor(Math.random() * (this.state.data.loops.length - 1));
                }
                this.setState({displayedPathIndex: rand_index});
            } else {
                let new_index = this.state.displayedPathIndex + change;
                if(new_index >= 0 && new_index < this.state.data.loops.length) {
                    this.setState({displayedPathIndex: new_index});
                }
            }
        }
    }

    setDistanceMode = (km) =>
    {
        this.setState({kilometers: km});
    }

    getLoops() {
        this.setState({loading: true});
        this.setState({requestError: ""});

        fetch(`http://127.0.0.1:5000/data?dist_min=${this.state.textBoxValues.min_dist}&dist_max=${this.state.textBoxValues.max_dist}&loc_lat=${this.state.usedPosition.lat}&loc_lon=${this.state.usedPosition.lng}&km=${this.state.kilometers}&count=${this.state.textBoxValues.count}`, { method: 'get', mode: 'cors' })
        .then(
            res => res.json()
        ).then(
            data => {
                this.setState({loading: false});
                if(data.loops.length > 0) {
                    this.setState({data: data});
                    this.setState({displayedPathIndex: 0});
                    this.setState({pathsExist: true});
                } else {
                    this.setState({requestError: "No routes were found. Try adjusting your distances or starting location."})
                    this.setState({pathsExist: false});
                }
            }
        ).catch((error) => {
            console.log(error);
            this.setState({loading: false});
            this.setState({requestError: "The request failed. Adjust your parameters and try again, or check console for error messages."});
        });
    }

    success = (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        
        this.setState({currentPosition: {lat:lat, lng:lon}});
    }

    error = () => {
        console.log("Could not get location");
        this.setState({currentPosition: {lat:51.505, lng:-0.09}});
    }
    
    MapDisplay = () => {
        //const activePath = this.state.displayedPathIndex !== -1 ? this.state.data.loops[this.state.displayedPathIndex].path : [];
        const activePath = this.state.data.loops !== undefined ? this.state.data.loops[this.state.displayedPathIndex] : {path: [], center: [], distance: 0.0}

        if(this.state.currentPosition.lat === undefined) { //await current position
            navigator.geolocation.getCurrentPosition(this.success, this.error);
            return (
                <div></div>
            );
        } else {
            return (
                <div>
                    <MapRenderer currentPosition={this.state.currentPosition} activePath={activePath} kilometers={this.state.kilometers} markerCallback={this.markerCallback}/>
                </div>
            );
        }
    }
    
    render(){

        const errorMessage = this.state.requestError === "" ? (<div></div>) : (<p className={styles.error}>{this.state.requestError}</p>);
        return(
            <div>
                <div className={styles.gradient}>
                    <img src={titleImg} alt="Running Routes" className={styles.titleimg}></img>
                </div>
                <this.MapDisplay/>
                {errorMessage}
                <div className={styles.container}>
                    <button className={styles.button} onClick={this.handleSubmit} disabled={this.state.loading}>
                        FIND ROUTES
                    </button>
                    <input
                        className={styles.input}
                        placeholder="Min Dist"
                        title="Minimum possible distance for a route"
                        type='number' 
                        onChange={e => this.handleInputChange(e, "min_dist")} //min distance
                    />
                    <input
                        className={styles.input}
                        placeholder="Max Dist"
                        title="Maximum possible distance for a route"
                        type='number' 
                        onChange={e => this.handleInputChange(e, "max_dist")} //max distance
                    />
                    <input
                        className={styles.input + " " + styles.short}
                        placeholder="#"
                        title="Amount of routes to find (automatic if blank)"
                        type='number' 
                        onChange={e => this.handleInputChange(e, "count")} //max distance
                    />
                    <button className={styles.button} onClick={() => this.cyclePaths(-1, false)} disabled={!this.state.pathsExist ? true : this.state.displayedPathIndex === 0}>PREV</button>
                    <button className={styles.button} onClick={() => this.cyclePaths(1, false)} disabled={!this.state.pathsExist ? true : this.state.displayedPathIndex === this.state.data.loops.length - 1}>NEXT</button>
                    <button className={styles.button} onClick={() => this.cyclePaths(0, true)} disabled={!this.state.pathsExist}>RANDOM</button>

                    <button className={styles.button} onClick={() => this.setDistanceMode(1)} disabled={this.state.kilometers}>KM</button>
                    <button className={styles.button} onClick={() => this.setDistanceMode(0)} disabled={!this.state.kilometers}>MI</button>
                </div>
                <div className={styles.textBlock}>
                    <p className={styles.paragraph}>
                        Running Routes is a simple tool that uses the depth first search (DFS) algorithm with OpenStreetMap data to find and display running routes in your area.<br/><br/>
                        Click on the map to change the location of the marker, which will serve as the starting and ending point for all routes found. Specify the desired distance range
                        with the two textboxes. If the amount of routes to search for is left blank, a number will be picked based on route length to optimize performance.<br/><br/>Routes will never
                        repeat any section of trail or road, so no routes will be found if the starting point is on a dead end. Be aware that large distances or routes in very dense areas
                        will take a long time to be calculated.
                    </p>
                </div>
            </div>
        )
    }
};

export default InputReader;