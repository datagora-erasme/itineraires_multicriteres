import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/home';
import { MainContextProvider } from './contexts/mainContext';
import React, { useEffect } from 'react';

function App() {
	
    // Install/Activate Matomo Tag Manager
    useEffect(() => {
        var _mtm = (window._mtm = window._mtm || []);
        _mtm.push({ 'mtm.startTime': new Date().getTime(), event: 'mtm.Start' });
        var d = document,
            g = d.createElement('script'),
            s = d.getElementsByTagName('script')[0];
        g.async = true;
        g.src = 'https://statweb.grandlyon.com/js/container_RCYhv7z3.js';
        s.parentNode.insertBefore(g, s);
    }, []);

    return (
        <MainContextProvider>
            <div className="App">
                <Router>
                    <Routes>
                        <Route exact path="/" element={<Home />} />
                    </Routes>
                </Router>
            </div>
        </MainContextProvider>
    );
}
export default App;
