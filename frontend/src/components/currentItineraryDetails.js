import React, { useContext, useEffect, useState } from "react";
import MainContext from "../contexts/mainContext";
import { FaHourglassStart, FaSnowflake, FaHotjar } from "react-icons/fa";
import { GiPathDistance } from "react-icons/gi";
import { TbFlowerOff, TbFlower } from "react-icons/tb";
import { HiSpeakerXMark, HiSpeakerWave } from "react-icons/hi2";
import { MdPhotoCamera, MdNoPhotography } from "react-icons/md";
import { BiX } from "react-icons/bi";

const CurrentItineraryDetails = ({ showMenu }) => {
    const { currentItinerary, filteredItinerariesFeatures, setShowCurrentItineraryDetails, ifScore, lenScore, criteria } = useContext(MainContext);
    const [details, setDetails] = useState({});

    useEffect(() => {
        if (currentItinerary) {
            const newDetails = {};
            currentItinerary.forEach((itinerary) => {
                const details = calculateItineraryDetails(itinerary);
                    newDetails[itinerary.idcriteria] = {
                        ...details,
                        name: itinerary.name,
                        color: itinerary.color,
                    };
                })

            setDetails(newDetails);
        }
    }, [currentItinerary, criteria]);

    //fonction qui calcule la distance et la durée d'un itinéraire
    const calculateItineraryDetails = (itinerary) => {
        let totalDistance = 0;
        itinerary.geojson.features.forEach((feat) => {
            totalDistance += feat.properties.length;
        });

        const distance = totalDistance > 1000 
            ? `${(Math.round(totalDistance) / 1000).toString()} km` 
            : `${Math.round(totalDistance).toString()} m`;

        let duration = Math.round(totalDistance * 60 / 4000);
        if (duration > 60) {
            const hours = Math.trunc(duration / 60);
            const minutes = duration % 60;
            duration = `${hours}h ${minutes}min`;
        } else {
            duration = `${duration}min`;
        }

        return { distance, duration };
    };

    const tourismeFeature = filteredItinerariesFeatures.find(feature => feature.id === 'tourisme');


    return (
        <div className={`${showMenu ? '' : 'hidden'} pt-5px md:block mt-4 md:mt-0 card md:card-details-desktop`}>
            <div className="item-align-end w-full md:flex justify-end cursor-default hidden">
                <BiX
                    className="w-6 h-6 -mr-1 cursor-pointer"
                    cursor-pointer
                    onClick={() => {
                        setShowCurrentItineraryDetails(false);
                    }}
                />
            </div>
            <div className="flex flex-col gap-4">
                {criteria.map((criterion, idx) => {
                    const shortDetail = details[criterion + 'length']; //itinéraire le plus court
                    const weightedDetail = details[criterion]; //itinéraire pondéré pour le critère
                    return (
                        <div key={idx}>
                            {/* Itinéraire le plus court (ligne en pointillé) */}
                            <ItineraryDetail detail={shortDetail} criterion={criterion} score={lenScore[idx]} isShortest={true} />

                            {/* Itinéraire pondéré (ligne pleine) */}
                            {criterion === 'tourisme' && tourismeFeature?.geojson.length === 0 ? (
                                <div className="mt-2 flex flex-col items-start gap-2">
                                    <h6 className="font-bold text-mainText">
                                        Nous n'avons pas trouvé de lieux touristiques sur votre trajet
                                    </h6>
                                </div>
                            ) : (
                                <ItineraryDetail detail={weightedDetail} criterion={criterion} score={ifScore[idx]} isShortest={false} />
                            )}
                            <hr className="mt-4"/>
                        </div>
                    );
                })}
            </div>

            {criteria.length > 0 ? (
                <div className="mt-2 flex flex-col items-start gap-2">
                    <h6 className="font-bold text-mainText">Sur votre chemin :</h6>
                    <ul className="flex flex-row gap-8 flex-wrap">
                        {filteredItinerariesFeatures.map(layer => {
                            if (layer.geojson.length !== 0) {
                                return (
                                    <li key={layer.id} className="flex flex-row gap-2 items-center">
                                        {layer.geojson.length}
                                        <img className="w-8 h-8" alt={`${layer.id}_icon`} src={layer.markerOption.iconUrl} />
                                    </li>
                                );
                            }
                            return null;
                        })}
                    </ul>
                </div>
            ) : (
                <div className="mt-2 flex flex-col items-start gap-2">
                    <h6 className="font-bold text-mainText">Veuillez sélectionner un critère pour effectuer une recherche</h6>
                </div>
            )}
        </div>
    );
};

const ItineraryDetail = ({ detail, criterion, score, isShortest }) => {
    if (!detail) return null;

    return (
        <div className="flex flex-col items-start w-full">
            <div className="flex w-full items-center place-content-between">
                <h6 className="font-bold text-mainText">{detail.name}</h6>
                <div className="flex items-center gap-1">
                    {renderIcon(criterion)}
                    <div
                        className={`w-[100px] ${isShortest ? "h-[5px]" : "h-[10px]"} flex flex-row gap-4 pl-4 ${getGradientClasses(criterion)}`}
                    >
                        {isShortest && Array(5).fill(0).map((_, i) => (
                            <div key={i} className="h-full w-[10px] bg-white"></div>
                        ))}
                    </div>
                    {renderEndIcon(criterion)}
                </div>
            </div>
            <div className="grid grid-cols-3 w-full">
                <div className="px-2 flex gap-1">
                    <GiPathDistance className="mt-1" /> {detail.distance}
                </div>
                <div className="px-2 flex">
                    <FaHourglassStart className="mt-1" /> {detail.duration}
                </div>
                <div className="px-2 flex gap-1">
                    {renderScoreIcon(criterion)} {score}/10
                </div>
            </div>
        </div>
    );
};

function renderIcon(criterion) {
    switch (criterion) {
        case "frais":
            return <FaHotjar className="mt-1 text-startGradientLegend" />;
        case "pollen":
            return <TbFlower className="mt-1 text-startGradientLegendPollen" />;
        case "bruit":
            return <HiSpeakerWave className="text-startGradientLegendBruit" />;
        case "tourisme":
            return <MdNoPhotography className="mt-1 text-startGradientLegendTourisme" />;
        default:
            return null;
    }
}

function renderEndIcon(criterion) {
    switch (criterion) {
        case "frais":
            return <FaSnowflake className="mt-1 text-endGradientLegend" />;
        case "pollen":
            return <TbFlowerOff className="mt-1 text-endGradientLegendPollen" />;
        case "bruit":
            return <HiSpeakerXMark className="text-endGradientLegendBruit" />;
        case "tourisme":
            return <MdPhotoCamera className="mt-1 text-endGradientLegendTourisme" />;
        default:
            return null;
    }
}

function getGradientClasses(criterion) {
    switch (criterion) {
        case "frais":
            return "bg-gradient-to-r from-startGradientLegend to-endGradientLegend";
        case "pollen":
            return "bg-gradient-to-r from-startGradientLegendPollen to-endGradientLegendPollen";
        case "bruit":
            return "bg-gradient-to-r from-startGradientLegendBruit to-endGradientLegendBruit";
        case "tourisme":
            return "bg-gradient-to-r from-startGradientLegendTourisme to-endGradientLegendTourisme";
        default:
            return "";
    }
}

function renderScoreIcon(criterion) {
    switch (criterion) {
        case "frais":
            return <FaSnowflake className="mt-1 text-black" />;
        case "pollen":
            return <TbFlowerOff className="mt-1 text-black" />;
        case "bruit":
            return <HiSpeakerXMark className="mt-1 text-black" />;
        case "tourisme":
            return <MdPhotoCamera className="mt-1 text-black" />;
        default:
            return null;
    }
}

export default CurrentItineraryDetails;