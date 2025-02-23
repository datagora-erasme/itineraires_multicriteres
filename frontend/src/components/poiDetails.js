import React, { useContext } from "react";
import MainContext from "../contexts/mainContext";
import {BiX} from "react-icons/bi"

const PoiDetails = ({showMenu}) => {
    const {poiDetails, setShowPoiDetails} = useContext(MainContext)

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

    return (
        <div className={`${showMenu ? '' : 'hidden'} md:block mt-4 md:mt-0 card md:card-details-desktop`}>
            <div
                className="absolute -ml-6 -mt-2 w-full md:flex justify-end cursor-pointer hidden"
                onClick={() => {
                    setShowPoiDetails(false);
                }}
            >
                <BiX className="w-6 h-6" />
            </div>
            <div className="flex flex-col gap-4">
                {poiDetails && (
                    <div className="flex flex-col gap-2">
                        <h3 className="mb-4 font-bold text-mainText">{poiDetails.properties.nom}</h3>
                        {poiDetails.properties.adresse !== null && poiDetails.properties.adresse !== "" && poiDetails.properties.commune !== null && poiDetails.properties.commune !== "" && (
                            <div className="w-full flex gap-1 items-center">
                                <img className="w-8 h-8" src="marker.svg" alt={poiDetails.properties.markerOption.iconUrl} />
                                <span className="flex items-center text-left">
                                    {poiDetails.properties.adresse},{'  ' + poiDetails.properties.commune}
                                </span>
                            </div>
                        )}
                        {poiDetails.properties.openinghours !== null && poiDetails.properties.openinghours !== "" && (
                            <div className="w-full flex gap-1 items-center">
                                <img className="w-8 h-8" src="clock.svg" alt={poiDetails.properties.markerOption.iconUrl} />
                                <span className="flex items-center text-left">
                                    {transformOpeningHours(poiDetails.properties.openinghours)}
                                </span>
                            </div>
                        )}
                        {poiDetails.properties.commentaire !== null && poiDetails.properties.commentaire !== "" && (
                            <div className="w-full flex gap-1 items-center">
                                <img className="w-8 h-8" src="informations.svg" alt={poiDetails.properties.markerOption.iconUrl} />
                                <span className="flex items-center text-left">{poiDetails.properties.commentaire}</span>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default PoiDetails;