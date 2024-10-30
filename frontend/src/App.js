import logo from './logo.svg';

import { MainDataDisplay } from './components/main_data_display';
import './App.css';


function App() {
  return (
    <main className="h-screen">
      <div className="h-full grid grid-cols-3 gap-2">
        <div className="h-20 col-span-3 bg-green-600">
          <p className="font-black text-5xl content-center ">
            Arena Flowchart Guide
          </p>
        </div>
        <div className="h-20 col-span-3 grid grid-cols-2 rows-span 1 bg-yellow-500">
          <div className="font-black text-2xl">
            Current Champion:
          </div>
          <img
            className="h-20"
            src="https://statics.koreanbuilds.net/tile_200x200/Twitch.webp"
            alt="new"
          />
        </div>
        <div className="col-span-1 h-20 font-bold bg-red-400">
          Current Build
        </div>
        <div className="h-full font-bold bg-orange-400">
          Choose Current Round
        </div>
        <div className="h-full font-bold bg-pink-500">
          Best Possible Options (Click what you chose)
        </div>
        <div className='h-full col-span-3'>
          <MainDataDisplay/>
        </div>
        
      </div>
    </main>
  );
}

export default App;
