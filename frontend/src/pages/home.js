
import React, {useState} from 'react';
import Map from '../components/map'

import Content from '../components/content';

function Home(){
    const [showMenu, setShowMenu] = useState(true)
    sessionStorage.clear() //Clear session storage after refreshing the page
    
    return (
        <div style={{position: 'relative'}} className="min-h-screen max-h-screen">
            <Content showMenu={showMenu} setShowMenu={setShowMenu}/>
            <Map/>
        
        </div>
    );
}

export default Home; 