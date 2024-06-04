import React, { useContext, useState } from 'react'
import ListLayers from './listLayers'
import CalculateItinerary from './calculateItinerary'
import FreshnessAroundUser from './freshnessAroundUser'
import { FaChevronUp, FaChevronDown } from "react-icons/fa";
import MainContext from '../contexts/mainContext';
import CurrentItineraryDetails from './currentItineraryDetails';
import PoiDetails from './poiDetails';
import HeadBand from './headband';
import BackButton from './backButton';


function Content({showMenu, setShowMenu}){
    const [showItineraryCalculation, setShowItineraryCalculation] = useState(false)
    
    const [showLayers, setShowLayers] = useState(false);

    const { history, setHistory, showCurrentItineraryDetails, 
        setShowCircle, setSelectedLayers, setCurrentItinerary, 
        setSelectedEndAddress, setEndAddress, setShowCurrentItineraryDetails, setZoomToUserPosition, showPoiDetails, setShowPoiDetails, showFindFreshness, setShowFindFreshness } = useContext(MainContext)

    return(
        <>  
            <div style={{zIndex:1000}} className="absolute md:top-8 bottom-0 flex flex-col gap-4 w-full p-8 md:pd-0 md:w-[400px] rounded-t-3xl md:gap-0 md:rounded-full bg-bgWhite md:bg-transparent">
                <div className="hidden md:block bg-bgWhite w-[300px] ml-[20px] p-4 absolute top-0 rounded-full font-bold text-xl drop-shadow-lg">Parcours à la carte</div>
                <div className="hidden md:block h-8 bg-bgWhite rounded-t-3xl"></div>
                <div className=" md:hidden flex flex-row justify-center">
                    <BackButton showMenu={showMenu}/>
                    <div className="h-[12px] w-[100px] bg-ligneModale rounded-3xl -mt-2 mb-2" onClick={() => setShowMenu(!showMenu)}></div>
                </div>
                {showCurrentItineraryDetails && <CurrentItineraryDetails showMenu={showMenu}/>}
                {showPoiDetails && <PoiDetails showMenu={showMenu}/>}
                <div className={`${showMenu ? "" : "hidden"} md:block md:top-8 bottom-0 flex flex-col gap-4 w-full md:pd-0 rounded-t-3xl md:gap-0`}>
                <button 
                    onClick={() => {
                        setShowItineraryCalculation(!showItineraryCalculation)
                        setShowFindFreshness(false)
                        setShowPoiDetails(false)
                        setShowLayers(false)
                        setHistory([...history, {fn: () => setShowItineraryCalculation(false)}])
                        setShowCircle(false)
                        setSelectedLayers([])
                        window.trackButtonClick("OpenCalculateItinerary")
                        }} 
                    className="main-btn main-btn-mobile md:main-btn-desktop md:rounded-none md:rounded-b-none md:border-b-2 md:border-b-gray-100">
                    {showItineraryCalculation ? (
                    <FaChevronUp className="hidden md:block text-gray-500 mt-1" />
                    ) : (
                    <FaChevronDown className="hidden md:block text-gray-500 mt-1" />
                    )}
                    <span>Calculer un itinéraire piéton</span>
                </button>
                {showItineraryCalculation && <CalculateItinerary showItineraryCalculation={showItineraryCalculation} setShowItineraryCalculation={setShowItineraryCalculation}/>}

                <button 
                    onClick={() => {
                        setShowFindFreshness(!showFindFreshness)
                        setShowItineraryCalculation(false)
                        setShowLayers(false)
                        setHistory([...history, {fn: () => setShowFindFreshness(false)}])
                        setShowCircle(true)
                        setZoomToUserPosition(true)
                        setCurrentItinerary(null)
                        setSelectedEndAddress(null)
                        setEndAddress("")
                        setShowCurrentItineraryDetails(false)
                        setSelectedLayers([])
                        window.trackButtonClick("OpenFindFreshness")
                    }} 
                    className="main-btn main-btn-mobile md:main-btn-desktop md:rounded-none md:border-b-2 md:border-b-gray-100"
                    >
                    {showFindFreshness ? (
                    <FaChevronUp className="hidden md:block text-gray-500 mt-1" />
                    ) : (
                    <FaChevronDown className="hidden md:block text-gray-500 mt-1" />
                    )}
                    <span>Trouver un lieu frais</span>
                </button>
                {showFindFreshness && <FreshnessAroundUser/>}

                <button 
                    onClick={() => {
                        setShowLayers(!showLayers)
                        setShowItineraryCalculation(false)
                        setShowFindFreshness(false)
                        setShowPoiDetails(false)
                        setHistory([...history, {fn: () => setShowLayers(false)}])
                        setCurrentItinerary(null)
                        setSelectedEndAddress(null)
                        setEndAddress("")
                        setShowCurrentItineraryDetails(false)
                        setShowCircle(false)
                        window.trackButtonClick("OpenLayers")
                    }} 
                    className="main-btn main-btn-mobile md:main-btn-desktop md:rounded-none md:border-b-2 md:border-b-gray-100">
                    {showLayers ? (
                    <FaChevronUp className="hidden md:block text-gray-500 mt-1" />
                    ) : (
                    <FaChevronDown className="hidden md:block text-gray-500 mt-1" />
                    )}
                    <span>Consulter la carte fraîcheur</span>
                </button>
                {showLayers && <ListLayers/>}
                
                <div className='cursor-pointer secondary-btn secondary-btn-mobile md:overflow-y-hidden md:main-btn-desktop md:rounded-t-none md:rounded-b-none md:rounded-b-3xl'>
                    <a 
                        target="_blank" 
                        rel="noopener noreferrer" 
                        href='https://datagora.erasme.org/projets/sortons-au-frais/'
                        >
                            En savoir plus
                        </a>
                </div>
                </div>
                <HeadBand/>
            </div>
        </>
    )
}

export default Content