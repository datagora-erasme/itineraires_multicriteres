import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from './pages/home';
import { MainContextProvider } from './contexts/mainContext';

function App() {
  return (
    <MainContextProvider>
      <div className="App">
        <Router>
          <Routes>
            <Route exact path = "/" element={<Home/>}/>
          </Routes>

        </Router>
      </div>
    </MainContextProvider>
  );
}
export default App;
