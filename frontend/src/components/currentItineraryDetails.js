import React, { useContext, useEffect, useState } from "react";
import MainContext from "../contexts/mainContext";
import { FaHourglassStart, FaSnowflake, FaHotjar } from "react-icons/fa";
import { GiPathDistance } from "react-icons/gi";
import { TbFlowerOff, TbFlower } from "react-icons/tb";
import { HiSpeakerXMark, HiSpeakerWave } from "react-icons/hi2";
import { MdPhotoCamera, MdNoPhotography } from "react-icons/md";
import {BiX} from "react-icons/bi"

const CurrentItineraryDetails = ({showMenu}) => {
    const { currentItinerary, filteredItinerariesFeatures, setShowCurrentItineraryDetails, ifScore, lenScore, criteria } = useContext(MainContext)
    const [details, setDetails] = useState([])

    useEffect(() => {
        if(currentItinerary){
            setDetails([])
            for(let it of currentItinerary){
                let tot = 0
                let dist = 0
                let duration = 0
                it.geojson.features.forEach((feat) => {
                    tot = tot + feat.properties.length
                })
                if(tot > 1000){
                    dist = (Math.round(tot)/1000).toString() + " km"
                } else {
                    dist = Math.round(tot).toString() + " m"
                }
                duration = Math.round(Math.round(tot) * 60 / 4000)
                if(duration > 60){
                    let hour = Math.trunc(duration/60)
                    let minutes = duration % 60
                    duration = hour.toString()+ "h " + minutes.toString() +"min"
                } else {
                    duration = duration.toString() + "min"
                }
                setDetails((det) => [...det, {id: it.id, name: it.name, color: it.color, distance: dist, duration: duration}])
            }

        }
    }, [currentItinerary])

    return(
        <div className={`${showMenu ? "" : "hidden"} md:block mt-4 md:mt-0 card md:card-details-desktop`}>
            <div 
                className="absolute w-full md:flex justify-end -mt-2 -ml-6 cursor-pointer hidden" 
                onClick={() =>{ 
                    setShowCurrentItineraryDetails(false)
                    }}
                >
                <BiX className="w-6 h-6"/>
            </div>
            <div className="flex flex-col gap-4">
                {details.map((det, i) => {
                if (criteria === "frais") {
                    return(
                        <div key={i} className="flex flex-col items-start w-full">
                            <div className="flex w-full items-center gap-6">
                                <h6 className="font-bold text-mainText">{det.name}</h6>
                                <div className="flex items-center gap-1">
                                <FaHotjar className="mt-1 text-startGradientLegend"/> 
                                <div className={`bg-gradient-to-r from-startGradientLegend to-endGradientLegend w-[100px] ${det.id === "LENGTH" ? "h-[5px]" : "h-[10px]"} flex flex-row gap-4 pl-4`}>
                                    {det.id === "LENGTH" && (
                                        <>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                        </>
                                    )}
                                </div> <FaSnowflake className="mt-1 text-endGradientLegend"/> </div>
                            </div>
                            <div className="flex gap-4">
                                <div className="px-2 flex gap-1"><GiPathDistance className="mt-1"/> {det.distance}</div>
                                <div className="px-2 flex"><FaHourglassStart className="mt-1"/> {det.duration}</div>
                                <div className="px-2 flex gap-1"><FaSnowflake className="mt-1 text-black"/> {det.id === "LENGTH" ? lenScore : ifScore}/10</div>
                            </div>
                        </div>
                    ) }

                if (criteria === "pollen") {
                    return(
                        <div key={i} className="flex flex-col items-start w-full">
                            <div className="flex w-full items-center gap-2">
                                <h6 className="font-bold text-mainText">{det.name}</h6>
                                <div className="flex items-center gap-1">
                                <TbFlower className="mt-1 text-startGradientLegendPollen"/>
                                <div className={`bg-gradient-to-r from-startGradientLegendPollen to-endGradientLegendPollen w-[100px] ${det.id === "LENGTH" ? "h-[5px]" : "h-[10px]"} flex flex-row gap-4 pl-4`}>
                                    {det.id === "LENGTH" && (
                                        <>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                        </>
                                    )}
                                </div> 
                                <TbFlowerOff className="mt-1 text-endGradientLegendPollen"/> </div>
                            </div>
                            <div className="flex gap-4">
                                <div className="px-2 flex gap-1"><GiPathDistance className="mt-1"/> {det.distance}</div>
                                <div className="px-2 flex"><FaHourglassStart className="mt-1"/> {det.duration}</div>
                                <div className="px-2 flex gap-1"><TbFlowerOff className="mt-1 text-black"/> {det.id === "LENGTH" ? lenScore : ifScore}/10</div>
                            </div>
                        </div>
                    ) }

                if (criteria === "bruit") {
                    return(
                        <div key={i} className="flex flex-col items-start w-full">
                            <div className="flex w-full items-center gap-3">
                                <h6 className="font-bold text-mainText">{det.name}</h6>
                                <div className="flex items-center gap-2">
                                    <HiSpeakerWave className="text-startGradientLegendBruit" />
                                    <div className={`bg-gradient-to-r from-startGradientLegendBruit to-endGradientLegendBruit w-[100px] ${det.id === "LENGTH" ? "h-[5px]" : "h-[10px]"} flex flex-row gap-4 pl-4`}>
                                        {det.id === "LENGTH" && (
                                            <>
                                                <div className="h-full w-[10px] bg-white"></div>
                                                <div className="h-full w-[10px] bg-white"></div>
                                                <div className="h-full w-[10px] bg-white"></div>
                                                <div className="h-full w-[10px] bg-white"></div>
                                                <div className="h-full w-[10px] bg-white"></div>
                                            </>
                                        )}
                                    </div>
                                    <HiSpeakerXMark className="text-endGradientLegendBruit" />
                                </div>

                            </div>
                            <div className="flex gap-4">
                                <div className="px-2 flex gap-1"><GiPathDistance className="mt-1"/> {det.distance}</div>
                                <div className="px-2 flex"><FaHourglassStart className="mt-1"/> {det.duration}</div>
                                <div className="px-2 flex gap-1"><HiSpeakerXMark className="mt-1 text-black"/> {det.id === "LENGTH" ? lenScore : ifScore}/10</div>
                            </div>
                        </div>
                    ) }

                    if (criteria === "tourisme") {
                        return(
                            <div key={i} className="flex flex-col items-start w-full">
                                <div className="flex w-full items-center gap-2">
                                    <h6 className="font-bold text-mainText">{det.name}</h6>
                                    <div className="flex items-center gap-1">
                                    <MdNoPhotography className="mt-1 text-startGradientLegendTourisme"/> 
                                    <div className={`bg-gradient-to-r from-startGradientLegendTourisme to-endGradientLegendTourisme w-[100px] ${det.id === "LENGTH" ? "h-[5px]" : "h-[10px]"} flex flex-row gap-4 pl-4` }>
                                        {det.id === "LENGTH" && (
                                            <>
                                                <div className="h-full w-[10px] bg-white"> </div>
                                                <div className="h-full w-[10px] bg-white"> </div>
                                                <div className="h-full w-[10px] bg-white"> </div>
                                                <div className="h-full w-[10px] bg-white"> </div>
                                                <div className="h-full w-[10px] bg-white"> </div>
                                            </>
                                        )}
                                    </div> <MdPhotoCamera className="mt-1 text-endGradientLegendTourisme"/> </div>
                                </div>
                                <div className="flex gap-4">
                                    <div className="px-2 flex gap-1"><GiPathDistance className="mt-1"/> {det.distance}</div>
                                    <div className="px-2 flex"><FaHourglassStart className="mt-1"/> {det.duration}</div>
                                    <div className="px-2 flex gap-1"><MdPhotoCamera className="mt-1 text-black"/> {det.id === "LENGTH" ? lenScore : ifScore}/10</div>
                                </div>
                            </div>
                        ) }
                })}
            
            </div>
            <div className="mt-2 flex flex-col items-start gap-2">
                <h6 className="font-bold text-mainText">Sur votre chemin : </h6>
                <ul className="flex flex-row gap-8 flex-wrap">
                    {
                        filteredItinerariesFeatures.map((layer) => {
                            if(layer.geojson.length !== 0){
                                return(
                                    <li className="flex flex-row gap-2 items-center">
                                        {layer.geojson.length}
                                        <img className="w-8 h-8" alt={`${layer.id}_icon`} src={layer.markerOption.iconUrl}/>
                                    </li>
                                )
                            }
                            return null
                        })
                    }
                </ul>
            </div>
        </div>
    )
}

export default CurrentItineraryDetails;