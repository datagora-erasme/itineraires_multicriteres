import React, {createContext, useState, useEffect} from "react"
import axios from 'axios'

const MainContext = createContext();

export const MainContextProvider = ({ children }) => {
    const [userPosition, setUserPosition] = useState(null)
    const [zoomToUserPosition, setZoomToUserPosition] = useState(false)
    const [zoomToItinerary, setZoomToItinerary] = useState(false)

    const [listLayers, setListLayers] = useState([])
    const [layers, setLayers] = useState([])
    const [selectedLayers, setSelectedLayers] = useState([])
    const [freshnessLayers, setFreshnessLayers] = useState([])

    const [filteredFreshnessFeatures ,setFilteredFreshnessFeatures] = useState([])
    const [filteredItinerariesFeatures, setFilteredItinerariesFeatures] = useState([])

    const [currentItinerary, setCurrentItinerary] = useState(null)
    const [showCurrentItineraryDetails, setShowCurrentItineraryDetails] = useState(false)
    const [showFindFreshness, setShowFindFreshness] = useState(false)

    const [startAddress, setStartAddress] = useState("");
    const [endAddress, setEndAddress] = useState("");
    const [selectedStartAddress, setSelectedStartAddress] = useState(null)
    const [selectedEndAddress, setSelectedEndAddress] = useState(null)

    const [isLayerLoading, setIsLayerLoading] = useState(false)

    const [userAddress, setUserAddress] = useState(null)

    const [history, setHistory] = useState([])

    const [radius, setRadius] = useState(1)

    const [showCircle, setShowCircle] = useState(false)

    const [showPoiDetails, setShowPoiDetails] = useState(false)

    const [poiDetails, setPoiDetails] = useState(null)

    const [ifScore, setIfScore] = useState([])

    const [lenScore, setLenScore] = useState([])

    const [criteria, setCriteria] = useState([]);

    // const calculateMeanScore = (itinerary, localcriteria) => {
    //   let scores;
    //   console.log(localcriteria)
    //   if (localcriteria === "frais") {
    //       scores = itinerary.geojson.features.map((feat) => feat.properties.freshness_score_13);
    //   } else if (localcriteria === "pollen") {
    //       scores = itinerary.geojson.features.map((feat) => feat.properties.pollen_score);
    //   } else if (localcriteria === "bruit") {
    //     scores = itinerary.geojson.features.map((feat) => feat.properties.bruit_score);
    //   } else if (localcriteria === "tourisme") {
    //     scores = itinerary.geojson.features.map((feat) => feat.properties.tourisme_score);
    //   }
    const calculateMeanScore = (itinerary, criteria) => {
      let scores;
      console.log("criteria calculatemeanscore", criteria)
      if (criteria === "frais") {
          scores = itinerary.geojson.features.map((feat) => feat.properties.freshness_score_13);
      } else if (criteria === "pollen") {
          scores = itinerary.geojson.features.map((feat) => feat.properties.pollen_score);
      } else if (criteria === "bruit") {
        scores = itinerary.geojson.features.map((feat) => feat.properties.bruit_score);
      } else if (criteria === "tourisme") {
        scores = itinerary.geojson.features.map((feat) => feat.properties.tourisme_score);
      }
      else {
          console.log("criteria not found")
          return  ;
      }
      const initialValue = 0;
      const sum = scores.reduce((accumulator, currentValue) => accumulator + currentValue, initialValue);
      return Math.round((sum / scores.length) * 10) / 10;
    }

    const roundItineraries = (itineraries) => { 
      return itineraries.map((it) => {
        return {
          ...it,
          geojson: {
            ...it.geojson,
            features: it.geojson.features.map((feat) => {
              return {
                ...feat,
                geometry: {
                  ...feat.geometry,
                  coordinates: feat.geometry.coordinates.map((coord) => {
                    return coord.map((co) => Math.round(co*100000)/100000)
                  })
                }
              }
            })
          }
        }
      })
    }

    useEffect(() => {
        async function fetchListLayers(){
            try{
                const response = await axios({
                    method:'get',
                    baseURL: `${process.env.REACT_APP_URL_SERVER}`,
                    url: "/data/",
                })
                setListLayers(response.data) 
            } catch (error){
                console.error(error)
            } 
        }
        setIsLayerLoading(true)
        fetchListLayers()
        setIsLayerLoading(false)
    }, [])

    useEffect(() => {
      async function fetchLayers(){
        const res = await axios.get(`${process.env.REACT_APP_URL_SERVER}/data/`, {
          params:{
              id: "all"
          }
        })
        setLayers(res.data)
      }
        fetchLayers()
    }, [])
    
    useEffect(() => {
        // Get user's current position using geolocation API
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            const { latitude, longitude } = pos.coords;
            setUserPosition([latitude, longitude]);
          },
          (err) => {
            console.log(err);
          }
        );
      }, []);

    useEffect(() => {
      async function fetchFreshnessLayers(){
        const fetchParcs = await axios.get(`${process.env.REACT_APP_URL_SERVER}/data/`, {
          params:{
              id: "parcs"
          }
      })
        //https://download.data.grandlyon.com/files/rdata/pvo_patrimoine_voirie.pvocameracriter/equipements_frais.json --> solution temporaire
        //https://download.data.grandlyon.com/ws/grandlyon/com_donnees_communales.equipementspublicsclimatises/all.json --> solution initiale
        const fetchFreshPlaces = await axios.get("https://download.data.grandlyon.com/files/rdata/sortons_au_frais/equipements_frais.json")
        const freshplaces = {
          id: "batiments_frais",
          geojson: {
            crs: {
              properties: {name: 'urn:ogc:def:crs:OGC:1.3:CRS84'},
              type: "name"
            },
            features: fetchFreshPlaces.data.values.map((val) => {
            return {
                geometry: {coordinates: [val.lon, val.lat], type:"Point"},
                properties: {
                  ...val,
                  markerOption: {
                    iconUrl: "building.svg",
                    iconRetinaUrl: "building.svg",
                    popupAnchor: [
                              0,
                              0
                          ],
                    iconSize: [
                              40,
                              40
                          ],
                    clusterCountStyle: "position:absolute;top:48px;left:0px;color:black;font-weight:bold;"
                  }
                },
                type: "Feature"
              }
              }),
            type: "FeatureCollection"
        },
        }
        setFreshnessLayers([fetchParcs.data, freshplaces])
      }
      fetchFreshnessLayers()
    }, [])

    useEffect(() => {
        if(userPosition){
            axios
            .get(
              `https://api-adresse.data.gouv.fr/reverse/?lon=${userPosition[1]}&lat=${userPosition[0]}`
            )
            .then((response) => {
              setUserAddress(response.data.features[0]);
            })
            .catch((error) => {
              console.log(error);
            });
        }
    }, [userPosition])


    useEffect(() => {
      if(currentItinerary){
        setZoomToItinerary(true);
        const roundIt = roundItineraries(currentItinerary);
        let newIfScore = [];
        let newLenScore = [];
        for (let i = 0; i < criteria.length; i++) {
          let k = i * 2;
          let ifScoreA = calculateMeanScore(currentItinerary[k + 1], criteria[i]);
          let lenScoreA = calculateMeanScore(currentItinerary[k], criteria[i]);
          newIfScore.push(ifScoreA);
          newLenScore.push(lenScoreA);
        }
        setIfScore(newIfScore);
        setLenScore(newLenScore);
        console.log("ifScore", newIfScore);
        console.log("lenScore", newLenScore);
        console.log("currentItinerary", currentItinerary);
      }
    }, [currentItinerary]);
    

    return(
        <MainContext.Provider
            value={{
                userPosition,
                setUserPosition,
                zoomToUserPosition, 
                setZoomToUserPosition,
                listLayers,
                setListLayers,
                selectedLayers,
                setSelectedLayers,
                currentItinerary,
                setCurrentItinerary,
                showCurrentItineraryDetails,
                setShowCurrentItineraryDetails,
                isLayerLoading,
                setIsLayerLoading,
                userAddress, 
                history, 
                setHistory,
                startAddress, 
                setStartAddress,
                endAddress,
                setEndAddress,
                selectedStartAddress,
                setSelectedStartAddress,
                selectedEndAddress,
                setSelectedEndAddress,
                radius,
                setRadius, 
                showCircle, 
                setShowCircle,
                zoomToItinerary,
                setZoomToItinerary,
                freshnessLayers,
                showPoiDetails,
                setShowPoiDetails,
                showFindFreshness,
                setShowFindFreshness,
                poiDetails, 
                setPoiDetails,
                layers,
                filteredFreshnessFeatures,
                setFilteredFreshnessFeatures,
                filteredItinerariesFeatures,
                setFilteredItinerariesFeatures, 
                ifScore,
                lenScore,
                roundItineraries,
                criteria,
                setCriteria
            }}
        >
            {children}
        </MainContext.Provider>
    );
};

export default MainContext;