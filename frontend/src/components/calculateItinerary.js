import React, { useCallback, useContext, useEffect, useState } from "react";
import axios from "axios";
import _debounce from 'lodash/debounce';
import { FaChevronDown, FaCheck, FaSnowflake } from "react-icons/fa";
import { HiSpeakerXMark } from "react-icons/hi2";
import { TbFlowerOff } from "react-icons/tb";
import { MdPhotoCamera } from "react-icons/md";

import { BiCurrentLocation } from "react-icons/bi";
import MainContext from "../contexts/mainContext";


const CalculateItinerary = ({ showItineraryCalculation, setShowItineraryCalculation }) => {
  const [startAddressSuggestions, setStartAddressSuggestions] = useState([]);
  const [endAddressSuggestions, setEndAddressSuggestions] = useState([]);
  const [showStartSuggestions, setShowStartSuggestions] = useState(false);
  const [showEndSuggestions, setShowEndSuggestions] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const {
    setCurrentItinerary, userAddress, history, setHistory, setShowCurrentItineraryDetails,
    selectedStartAddress, setSelectedStartAddress, selectedEndAddress, setSelectedEndAddress,
    startAddress, setStartAddress, endAddress, setEndAddress, setUserPosition, roundGeographicalCoordinatesOnItineraries,
    criteria, setCriteria
  } = useContext(MainContext);

  const handleStartAddressAPI = (query) => {
    axios
      .get(`https://download.data.grandlyon.com/geocoding/photon-bal/api?q=${query}`)
      .then((response) => {
        setStartAddressSuggestions(response.data.features);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleEndAddressAPI = (query) => {
    axios
      .get(`https://download.data.grandlyon.com/geocoding/photon-bal/api?q=${query}`)
      .then((response) => {
        setEndAddressSuggestions(response.data.features);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const debounceStartAddress = useCallback(_debounce(handleStartAddressAPI, 300), []);
  const debounceEndAddress = useCallback(_debounce(handleEndAddressAPI, 300), []);

  const handleStartAddressChange = (event) => {
    const value = event.target.value;
    let query = value.replace(/\s{2,}/g, ' ').replace(/ /g, "+");
    setStartAddress(value);
    setSelectedStartAddress(null);
    if (query.length > 3) {
      debounceStartAddress(query);
    } else {
      setStartAddressSuggestions([]);
    }
  };

  const handleEndAddressChange = (event) => {
    const value = event.target.value;
    let query = value.replace(/\s{2,}/g, ' ').replace(/ /g, "+");
    setEndAddress(value);
    setSelectedEndAddress(null);
    if (query.length > 3) {
      debounceEndAddress(query);
    } else {
      setEndAddressSuggestions([]);
    }
  };

  const addressName = ({ city, street, postcode, housenumber }) => {
    return `${housenumber ? housenumber : ""} ${street}, ${postcode} ${city.toUpperCase()}`;
  };

  const handleSelectStartAddress = (id) => {
    for (let address of startAddressSuggestions) {
      if (address.properties.osm_id === id) {
        setStartAddress(`${addressName(address.properties).slice(0, 30)}...`);
        setSelectedStartAddress(address);
        setStartAddressSuggestions([]);
      }
    }
  };

  const handleSelectEndAddress = (id) => {
    for (let address of endAddressSuggestions) {
      if (address.properties.osm_id === id) {
        setEndAddress(`${addressName(address.properties).slice(0, 30)}...`);
        setSelectedEndAddress(address);
        setEndAddressSuggestions([]);
      }
    }
  };

  const handlePreviousEndAddress = () => {

    const previousEndAddress = JSON.parse(sessionStorage.getItem('previousEndAddress'));
    setEndAddress(`${addressName(previousEndAddress.properties).slice(0, 30)}...`);
    setSelectedEndAddress(previousEndAddress);
    setEndAddressSuggestions([]);
  };

  const handleSelectUserAddress = () => {
    if (userAddress) {
      setStartAddress(`${userAddress.properties.label.slice(0, 30)}...`);
      setSelectedStartAddress(userAddress);
    } else {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          const { latitude, longitude } = pos.coords;
          setUserPosition([latitude, longitude]);
        },
        (err) => {
          console.log(err);
        }
      );
    }
  };



  const calculateItinerary = () => {
    setIsLoading(true);
    setShowCurrentItineraryDetails(false);
    axios.get(`${process.env.REACT_APP_URL_SERVER}/itinerary/`, {
      params: {
        start: {
          lat: selectedStartAddress.geometry.coordinates[1],
          lon: selectedStartAddress.geometry.coordinates[0]
        },
        end: {
          lat: selectedEndAddress.geometry.coordinates[1],
          lon: selectedEndAddress.geometry.coordinates[0]
        },
        //criteria : criteria ? criteria.join(',') : {}
        //criteria : criteria.map((n) => `${n}`).join('&')
        criteria
      }
    }).then((response) => {
      sessionStorage.setItem('previousEndAddress', JSON.stringify(selectedEndAddress));
      const roundIt = roundGeographicalCoordinatesOnItineraries(response.data);
      setCurrentItinerary(roundIt);
      setIsLoading(false);
      setShowItineraryCalculation(false);
      setShowCurrentItineraryDetails(true);
      setHistory([...history, {
        fn: () => {
          setShowCurrentItineraryDetails(false);
          setShowItineraryCalculation(true);
        }
      }]);
    }).catch((error) => {
      console.error(error);
    });
  };

  const handleEndFocus = () => {
    setShowEndSuggestions(true);
  };

  useEffect(() => {
    if (userAddress && startAddress === "") {
      setStartAddress(`${userAddress.properties.label.slice(0, 30)}...`);
      setSelectedStartAddress(userAddress);
    }

    if (sessionStorage?.getItem('previousEndAddress')) {
      handlePreviousEndAddress()
    }
  }, [userAddress]);

  const toggleCriteria = (criterion) => {
    if (criteria.includes(criterion)) {
      setCriteria(criteria.filter(c => c !== criterion));
    } else {
      setCriteria([...criteria, criterion]);
    }
  };

  return (
    <div className="card md:card-desktop">
      <button className="md:hidden card-title">
        <FaChevronDown className="text-gray-500 mt-1 hidden md:block" />
        <span>Calculer un itinéraire piéton</span>
      </button>
      <label htmlFor="startAddress" className="block mb-1 mt-4 flex">
        Départ
      </label>
      <div className="relative flex gap-2">
        <input
          type="text"
          id="startAddress"
          name="startAddress"
          value={startAddress}
          onChange={handleStartAddressChange}
          onFocus={() => setShowStartSuggestions(true)}
          onBlur={() => setTimeout(() => setShowStartSuggestions(false), 200)}
          className="main-input"
          placeholder="Adresse de départ"
        />
        {showStartSuggestions && <ul
          id="startAddressSuggestions"
          className="absolute z-10 w-full max-h-[200px] bg-white border-gray-300 rounded-md shadow-lg mt-12 md:mt-10 overflow-y-scroll"
          value={startAddress}
        >
          {startAddressSuggestions.map((suggestion) => {
            const name = addressName(suggestion.properties);
            return (
              <li key={suggestion.properties.osm_id} value={suggestion.properties.osm_id} onClick={() => handleSelectStartAddress(suggestion.properties.osm_id)}>
                {name.length > 40 ? `${name.slice(0, 40)}...` : name}
              </li>
            )
          })}
        </ul>}
        <BiCurrentLocation 
          size={30}
          className="mt-1 cursor-pointer" 
          onClick={() => {
            handleSelectUserAddress()
            window.trackButtonClick(`CalculateItinerary_UseUserPosition`);
          }} />
      </div>
      <label htmlFor="endAddress" className="block my-2 flex ">
        Arrivée
      </label>
      <div className="relative">
        <input
          type="text"
          id="endAddress"
          name="endAddress"
          value={endAddress}
          onChange={handleEndAddressChange}
          onFocus={() => handleEndFocus(true)}
          onBlur={() => setTimeout(() => handleEndFocus(false), 200)}
          className="main-input mb-4"
          placeholder="Adresse d'arrivée"
        />
        {showEndSuggestions && <ul
          id="endAddressSuggestions"
          className="absolute z-10 w-full max-h-[200px] bg-white border-gray-300 rounded-md shadow-lg mt-0 overflow-y-scroll"
          value={endAddress}
        >
          {endAddressSuggestions.map((suggestion) => {
            const name = addressName(suggestion.properties);
            return (
              <li key={suggestion.properties.osm_id} value={suggestion.properties.osm_id} onClick={() => handleSelectEndAddress(suggestion.properties.osm_id)}>
                {name.length > 40 ? `${name.slice(0, 40)}...` : name}
              </li>
            )
          })}
        </ul>}
      </div>

      <div>
        <span className="block mb-1 mt-4 flex">Critères</span>
        <div className="flex justify-center items-center mb-4 ">
          <button
            onClick={() => {
              toggleCriteria("frais")
              window.trackButtonClick(`CalculateItinerary_PlusAuFrais`)
            }}
            className={`main-btn inline-flex items-center mx-1 text-xs rounded-full transition duration-300 ${criteria.includes("frais") ? "bg-black text-white" : "bg-white text-black border border-gray-300"}`}
          >
            <FaSnowflake className="mr-1" /> Plus au frais
          </button>

          <button
            onClick={() => {
              toggleCriteria("pollen")
              window.trackButtonClick(`CalculateItinerary_MoinsDePollen`);
            }}
            className={`main-btn inline-flex items-center mx-1 text-xs rounded-full transition duration-300 ${criteria.includes("pollen") ? "bg-black text-white" : "bg-white text-black border border-gray-300"}`}
          >
            <TbFlowerOff className="mr-1" /> Moins de pollen
          </button>
          </div>
          <div className="flex justify-center items-center mb-4 ">
          <button
            onClick={() => {
              toggleCriteria("bruit")
              window.trackButtonClick(`CalculateItinerary_MoinsDeBruit`);
            }}
            className={`main-btn inline-flex items-center mx-1 text-xs rounded-full transition duration-300 ${criteria.includes("bruit") ? "bg-black text-white" : "bg-white text-black border border-gray-300"}`}
          >
            <HiSpeakerXMark className="mr-1" /> Moins de bruit
          </button>
          <button
            onClick={() => {
              toggleCriteria("tourisme")
              window.trackButtonClick(`CalculateItinerary_LieuxTouristiques`);
            }}
            className={`main-btn inline-flex items-center mx-1 text-xs rounded-full transition duration-300 ${criteria.includes("tourisme") ? "bg-black text-white" : "bg-white text-black border border-gray-300"}`}
          >
            <MdPhotoCamera className="mr-1" /> Lieux touristiques
          </button>
          </div>

        
        <div className="flex justify-center items-center">
          <button
            onClick={calculateItinerary}
            className={`main-btn ${!selectedStartAddress || !selectedEndAddress ? "bg-gray-300 hover:bg-gray-400" : "bg-primary md:opacity-80 hover:opacity-100"} text-mainText font-bold rounded-full transition duration-300`}
            disabled={!selectedStartAddress || !selectedEndAddress}
          >
            {isLoading ? (
              <div className="flex items-center gap-2">
                <span>En cours de chargement</span>
                <div className="w-6 h-6 rounded-full border-4 border-gray-300 border-t-primary animate-spin mr-3"></div>
              </div>
            ) : (
              <div className="flex items-center gap-2" onClick={() => window.trackButtonClick("ValidateCalculateItinerary")}>
                <span className="">Valider ma recherche </span>
                <FaCheck />
              </div>
            )}
          </button>
        </div>
      </div>
    </div>  
  );
};

export default CalculateItinerary;