import React, { useState } from "react";
import {FaInfoCircle} from "react-icons/fa";

function HeadBand(){
    const [showHeadBand, setShowHeadBand] = useState(false)
    return(
        <>
            <div style={{zIndex:1000}} className="bg-primary md:rounded-b-3xl w-full h-fit">
                <span className="hidden md:block">Ce site est une expérimentation.</span>
                <span className="hidden md:block">Partagez vos retours <a target="_blank" rel="noreferrer"  href="https://form.typeform.com/to/NkCgR8ie" className="text-mainText underline-offset-4 font-bold">ici</a></span>
            </div>

            <div className="fixed left-4 top-4 md:hidden flex flex-row items-center gap-2 min-h-[50px]">
                <div onClick={() => setShowHeadBand(!showHeadBand)} className="bg-primary rounded-full">
                        <FaInfoCircle className="w-10 h-10 text-mainText"/>
                </div>
                {showHeadBand &&
                    <div className="bg-primary p-4 rounded-full flex flex-col">
                        <span>Ce site est une expérimentation.</span>
                        <span className="">Partagez vos retours <a target="_blank" rel="noreferrer"  href="https://form.typeform.com/to/NkCgR8ie" className="text-mainText underline-offset-4 font-bold">ici</a></span>
                    </div> 
                }
            </div>
        </>
    )

}

export default HeadBand;