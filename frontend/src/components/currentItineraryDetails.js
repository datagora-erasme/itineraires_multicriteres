import React, { useContext } from 'react';
import MainContext from '../contexts/mainContext';
import { FaHourglassStart, FaSnowflake, FaHotjar } from 'react-icons/fa';
import { GiPathDistance } from 'react-icons/gi';
import { TbFlowerOff, TbFlower } from 'react-icons/tb';
import { HiSpeakerXMark, HiSpeakerWave, HiBolt } from 'react-icons/hi2';
import { MdPhotoCamera, MdNoPhotography } from 'react-icons/md';
import { BiX } from 'react-icons/bi';

const roundScore = score => Math.round(score * 10) / 10;

const itineraryDistance = itinerary => {
    let totalDistance = 0;
    itinerary.geojson.features.forEach(feat => {
        totalDistance += feat.properties.length;
    });
    return totalDistance;
};

const formatDistance = distance => {
    return distance > 1000 ? `${(Math.round(distance) / 1000).toString()} km` : `${Math.round(distance).toString()} m`;
};

const itineraryDuration = totalDistance => Math.round((totalDistance * 60) / 4000);

const formatDuration = duration => {
    if (duration > 60) {
        const hours = Math.trunc(duration / 60);
        const minutes = duration % 60;
        return `${hours}h ${minutes}min`;
    } else {
        return `${duration}min`;
    }
};

const CurrentItineraryDetails = ({ showMenu }) => {
    const { currentItinerary, filteredItinerariesFeatures, setShowCurrentItineraryDetails } = useContext(MainContext);

    const currentItinerariesWithExtraDetails = currentItinerary.map(itinerary => {
        const totalDistance = itineraryDistance(itinerary);
        return {
            ...itinerary,
            distance: formatDistance(totalDistance),
            duration: formatDuration(itineraryDuration(totalDistance)),
        };
    });

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
                {currentItinerariesWithExtraDetails.map((itinerary, index) => {
                    return itinerary.id === 'IF' ? (
                        <div key={index}>
                            {/* Itinéraire pondéré (ligne pleine) */}
                            {itinerary.idcriteria === 'tourisme' && tourismeFeature?.geojson.length === 0 ? (
                                <div className="mt-2 flex flex-col items-start gap-2">
                                    <h6 className="font-bold text-mainText">
                                        Nous n'avons pas trouvé de lieux touristiques sur votre trajet
                                    </h6>
                                </div>
                            ) : (
                                <ItineraryDetail itinerary={itinerary} />
                            )}
                            <hr className="mt-4" />
                        </div>
                    ) : (
                        <div key={index}>
                            {/* Itinéraire le plus court (ligne en pointillé) */}
                            <ShortestItineraryDetail itinerary={itinerary} />
                            <hr className="mt-4" />
                        </div>
                    );
                })}
            </div>

            {currentItinerariesWithExtraDetails.filter(itineraries => itineraries.id === "IF").length > 0 ? (
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
                    <h6 className="font-bold text-mainText">Veuillez sélectionner un critère avant d'effectuer une recherche</h6>
                </div>
            )}
        </div>
    );
};

const ItineraryDetail = ({ itinerary }) => {
    if (!itinerary) return null;

    return (
        <div className="flex flex-col items-start w-full">
            <div className="flex w-full items-center place-content-between">
                <h6 className="font-bold text-mainText">{itinerary.name}</h6>
                <div className="flex items-center gap-1">
                    {renderIcon(itinerary.idcriteria)}
                    <div className={`w-[100px] h-[10px] flex flex-row gap-4 pl-4 ${getGradientClasses(itinerary.idcriteria)}`}></div>
                    {renderEndIcon(itinerary.idcriteria)}
                </div>
            </div>
            <div className="grid grid-cols-3 w-full">
                <div className="px-2 flex gap-1">
                    <GiPathDistance className="mt-1" /> {itinerary.distance}
                </div>
                <div className="px-2 flex">
                    <FaHourglassStart className="mt-1" /> {itinerary.duration}
                </div>
                <div className="px-2 flex gap-1">
                    {renderScoreIcon(itinerary.idcriteria)} {roundScore(itinerary.score[itinerary.idcriteria])}/10
                </div>
            </div>
        </div>
    );
};

const ShortestItineraryDetail = ({ itinerary }) => {
    if (!itinerary) return null;

    return (
        <div className="flex flex-col items-start w-full">
            <div className="flex w-full items-center place-content-between">
                <h6 className="font-bold text-mainText">{itinerary.name}</h6>
                <div className="flex items-center gap-1">
                    {renderIcon(itinerary.idcriteria)}
                    <div className={`w-[100px] h-[5px] flex flex-row gap-4 pl-4 bg-black`}>
                        {Array(5)
                            .fill(0)
                            .map((_, i) => (
                                <div key={i} className="h-full w-[10px] bg-white"></div>
                            ))}
                    </div>
                    {renderEndIcon(itinerary.idcriteria)}
                </div>
            </div>
            <div className="grid grid-cols-3 w-full items-center">
                <div className="px-2 flex gap-1">
                    <GiPathDistance className="mt-1" /> {itinerary.distance}
                </div>
                <div className="px-2 flex">
                    <FaHourglassStart className="mt-1" /> {itinerary.duration}
                </div>
                <div className="flex flex-col w-full">
                    {itinerary.score.map(criterion => (
                        <div className="px-2 flex gap-1">
                            {renderScoreIcon(Object.keys(criterion)[0])} {roundScore(Object.values(criterion)[0])}/10
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

function renderIcon(criterion) {
    switch (criterion) {
        case 'frais':
            return <FaHotjar className="mt-1 text-startGradientLegend" />;
        case 'pollen':
            return <TbFlower className="mt-1 text-startGradientLegendPollen" />;
        case 'bruit':
            return <HiSpeakerWave className="text-startGradientLegendBruit" />;
        case 'tourisme':
            return <MdNoPhotography className="mt-1 text-startGradientLegendTourisme" />;
        case 'length':
            return <HiBolt className="mt-1 text-black" />;
        default:
            return null;
    }
}

function renderEndIcon(criterion) {
    switch (criterion) {
        case 'frais':
            return <FaSnowflake className="mt-1 text-endGradientLegend" />;
        case 'pollen':
            return <TbFlowerOff className="mt-1 text-endGradientLegendPollen" />;
        case 'bruit':
            return <HiSpeakerXMark className="text-endGradientLegendBruit" />;
        case 'tourisme':
            return <MdPhotoCamera className="mt-1 text-endGradientLegendTourisme" />;
        case 'length':
            return <HiBolt className="mt-1 text-black" />;
        default:
            return null;
    }
}

function getGradientClasses(criterion) {
    switch (criterion) {
        case 'frais':
            return 'bg-gradient-to-r from-startGradientLegend to-endGradientLegend';
        case 'pollen':
            return 'bg-gradient-to-r from-startGradientLegendPollen to-endGradientLegendPollen';
        case 'bruit':
            return 'bg-gradient-to-r from-startGradientLegendBruit to-endGradientLegendBruit';
        case 'tourisme':
            return 'bg-gradient-to-r from-startGradientLegendTourisme to-endGradientLegendTourisme';
        default:
            return '';
    }
}

function renderScoreIcon(criterion) {
    switch (criterion) {
        case 'frais':
            return <FaSnowflake className="mt-1 text-black" />;
        case 'pollen':
            return <TbFlowerOff className="mt-1 text-black" />;
        case 'bruit':
            return <HiSpeakerXMark className="mt-1 text-black" />;
        case 'tourisme':
            return <MdPhotoCamera className="mt-1 text-black" />;
        default:
            return null;
    }
}

export default CurrentItineraryDetails;
