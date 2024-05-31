import React, { useContext } from "react";
import { FaArrowLeft } from "react-icons/fa";
import MainContext from "../contexts/mainContext";

const BackButton = ({showMenu}) => {
    const { history, setHistory } = useContext(MainContext)
    return(
        <button 
            style={{zIndex:1000}} 
            className={`absolute rounded-full bg-primary p-4 px-6 shadow-lg -top-6 left-1 md:hidden ${(history.length === 0 || !showMenu) ? "hidden" : ""}`}
            onClick={() => {
                history[history.length -1].fn()
                setHistory(history.slice(0,-1))
            }}
            >
            <FaArrowLeft className="mt-1"/>
        </button>
    )
}

export default BackButton;