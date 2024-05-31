import React, { useContext } from 'react'
import { FaChevronDown } from "react-icons/fa";
import MainContext from '../contexts/mainContext';

function ListLayers(){

    const { listLayers, selectedLayers, setSelectedLayers, isLayerLoading } = useContext(MainContext)  

    function handleCheckBoxList(event){
        const {value, checked} = event.target;
        if(checked){
            setSelectedLayers((prevSelectedLayers) => [...prevSelectedLayers, value]);
        } else {
            const updatedSelectedLayers = selectedLayers.filter((layerId) => layerId !== value)
            setSelectedLayers(updatedSelectedLayers)
        }
    }

    return (
        <div className="card md:card-desktop">
        <button
          className="md:hidden card-title"
        >
        {isLayerLoading && <div class="w-6 h-6 rounded-full border-4 border-gray-300 border-t-blue-500 animate-spin mr-3"></div>}
          <FaChevronDown className="text-gray-500 mt-1 hidden md:block" />
          <span className="text-lg font-bold mr-2">Afficher sur la carte</span>
        </button>
        {listLayers.length !== 0 ? (
            <ul className="mt-2 grid grid-cols-3">
              {listLayers.map((layer) => {
                console.log("Layer : ", layer)
                return (
                  <li key={layer.id} className="" onClick={() => window.trackButtonClick(`ShowLayer_${layer.id}`)}>
                    <label htmlFor={layer.id} className="ml-2 flex flex-col items-center text-xs gap-2">
                      <input
                        type="checkbox"
                        id={layer.id}
                        value={layer.id}
                        checked={selectedLayers.includes(layer.id)}
                        onChange={handleCheckBoxList}
                        disabled={isLayerLoading}
                        className="hidden"
                      />
                      <div id={`img_${layer.id}`} className='border-solid border-2 rounded-full p-4 hover:bg-gray-100 cursor-pointer'>
                        <img
                          className="w-8 h-8"
                          src={layer.marker_option.iconUrl}
                          alt="Checkbox"
                          onClick={(e) => {
                            const checkbox = document.getElementById(layer.id);
                            if (checkbox) {
                              checkbox.checked = !checkbox.checked;
                              const img = document.getElementById(`img_${layer.id}`)
                              if(checkbox.checked){
                                img.className = 'bg-gray-300 border-solid border-2 rounded-full p-4 cursor-pointer'
                              } else {
                                img.className = 'border-solid border-2 rounded-full p-4 hover:bg-gray-100 cursor-pointer'
                              }

                              handleCheckBoxList(e);
                            }
                          }}
                        />
                      </div>
                      {layer.name}
                    </label>
                  </li>
                );
              })}
            </ul>
          ) : (
            "Loading..."
          )}
      </div>
      );
    
      
}

export default ListLayers