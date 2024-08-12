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
    const [shortestItinerary, setShortestItinerary] = useState(null);

    useEffect(() => {
        if (Array.isArray(currentItinerary) && currentItinerary.length > 0 && criteria.length > 0) {
            let shortest = null;

            for (let it of currentItinerary) {
                let tot = 0;
                let dist = "";
                let duration = 0;

                //calculer la longueur totale
                it.geojson.features.forEach((feat) => {
                    tot += feat.properties.length;
                });

                //calculer la distance
                dist = tot > 1000 ? (Math.round(tot) / 1000).toString() + " km" : Math.round(tot).toString() + " m";

                //calculer la durée
                duration = Math.round((Math.round(tot) * 60) / 4000);
                duration = duration > 60 ? `${Math.trunc(duration / 60)}h ${duration % 60}min` : `${duration}min`;

                if (!shortest || tot < shortest.tot) {
                    shortest = { id: it.id, name: it.name, distance: dist, duration: duration, tot: tot };
                }
            }

            setShortestItinerary(shortest);
        }
    }, [currentItinerary, criteria]);

    const renderCriterion = (criterion, score) => {
        let startIcon, endIcon, gradientClass;

        switch (criterion) {
            case "frais":
                startIcon = <FaHotjar className="mt-1 text-startGradientLegend" />;
                endIcon = <FaSnowflake className="mt-1 text-endGradientLegend" />;
                gradientClass = "from-startGradientLegend to-endGradientLegend";
                break;
            case "pollen":
                startIcon = <TbFlower className="mt-1 text-startGradientLegendPollen" />;
                endIcon = <TbFlowerOff className="mt-1 text-endGradientLegendPollen" />;
                gradientClass = "from-startGradientLegendPollen to-endGradientLegendPollen";
                break;
            case "bruit":
                startIcon = <HiSpeakerWave className="text-startGradientLegendBruit" />;
                endIcon = <HiSpeakerXMark className="text-endGradientLegendBruit" />;
                gradientClass = "from-startGradientLegendBruit to-endGradientLegendBruit";
                break;
            case "tourisme":
                startIcon = <MdNoPhotography className="mt-1 text-startGradientLegendTourisme" />;
                endIcon = <MdPhotoCamera className="mt-1 text-endGradientLegendTourisme" />;
                gradientClass = "from-startGradientLegendTourisme to-endGradientLegendTourisme";
                break;
            default:
                return null;
        }

        return (
            <div key={criterion} className="flex flex-col items-start w-full">
                <div className="flex w-full items-center gap-6">
                    <h6 className="font-bold text-mainText">{criterion.charAt(0).toUpperCase() + criterion.slice(1)}</h6>
                    <div className="flex items-center gap-1">
                        {startIcon}
                        <div className={`bg-gradient-to-r ${gradientClass} w-[100px] h-[10px] flex flex-row gap-4 pl-4`}>
                            <div className="h-full w-[10px] bg-white"> </div>
                        </div>
                        {endIcon}
                    </div>
                </div>
                <div className="flex gap-4">
                    <div className="px-2 flex gap-1">{startIcon} {score}/10</div>
                </div>
            </div>
        );
    };

    return (
        <div className={`${showMenu ? "" : "hidden"} md:block mt-4 md:mt-0 card md:card-details-desktop`}>
            <div
                className="absolute w-full md:flex justify-end -mt-2 -ml-6 cursor-pointer hidden"
                onClick={() => setShowCurrentItineraryDetails(false)}
            >
                <BiX className="w-6 h-6" />
            </div>
            <div className="flex flex-col gap-4">
                {shortestItinerary ? (
                    <>
                        {/* afficher l'itinéraire le plus court */}
                        <div className="flex flex-col items-start w-full">
                            <div className="flex w-full items-center gap-6">
                                <h6 className="font-bold text-mainText">{shortestItinerary.name}</h6>
                                <div className="flex items-center gap-1">
                                    {criteria.length > 0 && (
                                        <>
                                            {criteria[0] === "frais" && <FaHotjar className="mt-1 text-startGradientLegend" />}
                                            {criteria[0] === "pollen" && <TbFlower className="mt-1 text-startGradientLegendPollen" />}
                                            {criteria[0] === "bruit" && <HiSpeakerWave className="text-startGradientLegendBruit" />}
                                            {criteria[0] === "tourisme" && <MdNoPhotography className="mt-1 text-startGradientLegendTourisme" />}
                                            <div className={`bg-gradient-to-r ${criteria[0] === "frais" ? "from-startGradientLegend to-endGradientLegend" : ""} 
                                                ${criteria[0] === "pollen" ? "from-startGradientLegendPollen to-endGradientLegendPollen" : ""}
                                                ${criteria[0] === "bruit" ? "from-startGradientLegendBruit to-endGradientLegendBruit" : ""}
                                                ${criteria[0] === "tourisme" ? "from-startGradientLegendTourisme to-endGradientLegendTourisme" : ""}
                                                w-[100px] h-[10px] flex flex-row gap-4 pl-4`}>
                                                <div className="h-full w-[10px] bg-white"> </div>
                                            </div>
                                        </>
                                    )}
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <div className="px-2 flex gap-1"><GiPathDistance className="mt-1" /> {shortestItinerary.distance}</div>
                                <div className="px-2 flex"><FaHourglassStart className="mt-1" /> {shortestItinerary.duration}</div>
                            </div>
                        </div>

                        {/* afficher les scores des critères pour l'itinéraire le plus court */}
                        {criteria.map((criterion, i) => (
                            <React.Fragment key={i}>
                                {renderCriterion(criterion, criterion === "frais" ? ifScore : lenScore)}
                            </React.Fragment>
                        ))}
                    </>
                ) : (
                    <div className="flex justify-center items-center p-4">
                        <p className="text-mainText">Aucun itinéraire disponible.</p>
                    </div>
                )}

                {/* afficher les autres itinéraires avec les critères */}
                {Array.isArray(currentItinerary) && currentItinerary.map((itinerary, index) => {
                    if (itinerary.id !== shortestItinerary?.id) {
                        let totalLength = itinerary.geojson.features.reduce((acc, feat) => acc + feat.properties.length, 0);
                        let dist = totalLength > 1000 ? (Math.round(totalLength) / 1000).toString() + " km" : Math.round(totalLength).toString() + " m";
                        let duration = Math.round((Math.round(totalLength) * 60) / 4000);
                        duration = duration > 60 ? `${Math.trunc(duration / 60)}h ${duration % 60}min` : `${duration}min`;

                        return (
                            <div key={index} className="flex flex-col items-start w-full">
                                <div className="flex w-full items-center gap-6">
                                    <h6 className="font-bold text-mainText">{itinerary.name}</h6>
                                    <div className="flex items-center gap-1">
                                        {criteria.length > 0 && (
                                            <>
                                                {criteria[0] === "frais" && <FaHotjar className="mt-1 text-startGradientLegend" />}
                                                {criteria[0] === "pollen" && <TbFlower className="mt-1 text-startGradientLegendPollen" />}
                                                {criteria[0] === "bruit" && <HiSpeakerWave className="text-startGradientLegendBruit" />}
                                                {criteria[0] === "tourisme" && <MdNoPhotography className="mt-1 text-startGradientLegendTourisme" />}
                                                <div className={`bg-gradient-to-r ${criteria[0] === "frais" ? "from-startGradientLegend to-endGradientLegend" : ""} 
                                                    ${criteria[0] === "pollen" ? "from-startGradientLegendPollen to-endGradientLegendPollen" : ""}
                                                    ${criteria[0] === "bruit" ? "from-startGradientLegendBruit to-endGradientLegendBruit" : ""}
                                                    ${criteria[0] === "tourisme" ? "from-startGradientLegendTourisme to-endGradientLegendTourisme" : ""}
                                                    w-[100px] h-[10px] flex flex-row gap-4 pl-4`}>
                                                    <div className="h-full w-[10px] bg-white"> </div>
                                                </div>
                                            </>
                                        )}
                                    </div>
                                </div>
                                <div className="flex gap-4">
                                    <div className="px-2 flex gap-1"><GiPathDistance className="mt-1" /> {dist}</div>
                                    <div className="px-2 flex"><FaHourglassStart className="mt-1" /> {duration}</div>
                                </div>
                            </div>
                        );
                    }
                    return null;
                })}
            </div>
        </div>
    );
};

export default CurrentItineraryDetails;
