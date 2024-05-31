import React, { useContext, useState } from "react";
import MainContext from "../contexts/mainContext";
import { FaCheck } from "react-icons/fa";
import L from "leaflet"
import axios from "axios";
import {BiX} from "react-icons/bi"

const PoiDetails = ({showMenu}) => {

    const [isLoading, setIsLoading] = useState(false)
    const {poiDetails, setCurrentItinerary, setShowCircle, setShowPoiDetails, setShowCurrentItineraryDetails, selectedStartAddress, history, setHistory, roundItineraries} = useContext(MainContext)

    const transformOpeningHours = (openinghours) => {
        const new_s = openinghours.split(";")
        return (
            <span>
                {
                    new_s.map((s,i) => {
                        return(
                            <span key={i}>
                                {s} <br/>
                            </span>
                        )
                    })
                }
            </span>
        )
    }

    const calculateItinerary = () => {
        let coordinates;
        if(poiDetails.geometry.type === "Polygon" || poiDetails.geometry.type === "MultiPolygon"){
            const layer = L.geoJSON(poiDetails)
            const bounds = layer.getBounds()
            const centroid = bounds.getCenter()

            coordinates = [centroid.lat, centroid.lng]
        } else if(poiDetails.geometry.type === "Point"){
            coordinates = [poiDetails.geometry.coordinates[1], poiDetails.geometry.coordinates[0]]
        }
        setIsLoading(true)
        axios({
            method:'get',
            baseURL: `${process.env.REACT_APP_URL_SERVER}`,
            url: "/itinerary/",
            params: {
                start: {
                    lat: selectedStartAddress.geometry.coordinates[1], 
                    lon: selectedStartAddress.geometry.coordinates[0]
                },
                end: {
                    lat : coordinates[0],
                    lon : coordinates[1]
                }
            }
        }).then((response) => {
            const roundIt = roundItineraries(response.data)
            setCurrentItinerary(roundIt)
            setShowPoiDetails(false)
            setShowCurrentItineraryDetails(true)
            setIsLoading(false)
            setShowCircle(false)
            setHistory([...history, {fn: () => {
                setShowCurrentItineraryDetails(false)
                setShowPoiDetails(true)
            }}])
        }).catch((error) => {
            console.error(error)
        })
    }

    return(
        <div className={`${showMenu ? "": "hidden"} md:block mt-4 md:mt-0 card md:card-details-desktop`}>
            <div 
                className="absolute -ml-6 -mt-2 w-full md:flex justify-end cursor-pointer hidden" 
                onClick={() =>{ 
                    setShowPoiDetails(false)
                    }}
                >
                <BiX className="w-6 h-6"/>
            </div>
            <div className="flex flex-col gap-4">
                {poiDetails && (
                    <div className="flex flex-col gap-2"> 
                        <h3 className="mb-4 font-bold text-mainText">{poiDetails.properties.nom}</h3>
                        {poiDetails.properties.adresse != null && poiDetails.properties.commune != null && <div className="w-full flex gap-1 items-center">
                            <img className="w-8 h-8" src="marker.svg" alt={poiDetails.properties.markerOption.iconUrl}/>
                            <span className="flex items-center text-left">
                                {poiDetails.properties.adresse},   
                                {"  " + poiDetails.properties.commune}
                            </span>
                        </div>}
                        {poiDetails.properties.openinghours != null && <div className="w-full flex gap-1 items-center">
                            <img className="w-8 h-8" src="clock.svg" alt={poiDetails.properties.markerOption.iconUrl}/>
                            <span className="flex items-center text-left">
                                {transformOpeningHours(poiDetails.properties.openinghours)}
                            </span>
                        </div>}
                        {poiDetails.properties.commentaire != null && <div className="w-full flex gap-1 items-center">
                            <img className="w-8 h-8" src="informations.svg" alt={poiDetails.properties.markerOption.iconUrl}/>
                            <span className="flex items-center text-left">
                                {poiDetails.properties.commentaire}
                            </span>
                        </div>}
                    </div>
                )}
                <div className="flex justify-center items-center">
                <button onClick={calculateItinerary} 
                className={` main-btn bg-primary md:opacity-80 hover:opacity-100 text-mainText font-bold rounded-full transition duration-300`}
                >
                {isLoading ? (
                    <div className="flex items-center gap-2">
                    <span>En cours de chargement</span>
                    <div className="w-6 h-6 rounded-full border-4 border-gray-300 border-t-primary animate-spin mr-3"></div>
                    </div>
                ) : (
                    <div className="flex items-center gap-2" onClick={() => window.trackButtonClick("ValidateCalculateItinerary")}>
                    <span className="">Valider ma recherche </span>
                    <FaCheck/>
                    </div>
                )}
                </button>
                </div>
            </div>
        </div>
    )
}

export default PoiDetails;