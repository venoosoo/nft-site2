import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Header from './header';
import Card from './card';
import Menu from './menu';

function getRandomInt(min, max) {
  // min and max are inclusive
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}


export default function Greeting() {
  const navigate = useNavigate();
  const location = useLocation();

  const params = new URLSearchParams(location.search);
  const bot = params.get('bot');
  const gift = params.get('gift');
  const urlParams = new URLSearchParams(window.location.search);

  const collections = [ "lootbag", "scaredcat", "swisswatch", "heartlocket", "partysparkler", "snoopdogg", "perfumebottle"]


  return (
    <div className="h-screen relative font-sans overflow-auto bg-[#121921] text-white">
      <Header />
      <div className='flex ml-6 mt-5 space-x-3 text-2xl overflow-x-auto scroll-smooth [scrollbar-width:none] [-ms-overflow-style:none] text-gray-400 font-bold' >
        <button className='whitespace-nowrap text-white'>Все подарки</button>
        <button>Коллекции</button>
        <button>Наборы</button>
      </div>
      <div className='ml-6 mt-4 flex items-center'>
        <div className='bg-[#242E3A]  p-2 rounded-3xl outline outline-2 outline-gray-700 flex items-center'>
          <div className='ml-1 mr-2'>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-3">
              <path strokeLinecap="round" strokeLinejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
          </div>
          <input className='text-white text-sm w-[50%] flex-1 bg-[#242E3A]' placeholder='Быстрый поиск' type='text'></input>
        </div>
        <div className='ml-3 bg-[#242E3A] outline outline-2 outline-gray-700 px-4 text-slate-300 text-[12px] py-2 rounded-3xl'>
          <button className=''>
            Активность
          </button>
        </div>
        <div>
          <button className='flex outline outline-2 outline-gray-700 p-1 mr-2 bg-[#242E3A] rounded-full ml-3'>
            <div className=''>
              <svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="5" y="5" width="14" height="3" rx="1" fill="#CFCFCF"/><rect x="5" y="9.5" width="6.5" height="4" rx="1" fill="#CFCFCF"/><rect x="12.5" y="9.5" width="6.5" height="4" rx="1" fill="#CFCFCF"/><rect x="5" y="14.5" width="6.5" height="4" rx="1" fill="#CFCFCF"/><rect x="12.5" y="14.5" width="6.5" height="4" rx="1" fill="#CFCFCF"/></svg>
            </div>
          </button>
        </div>
      </div>
      <div className='ml-7 mt-4 flex items-center gap-3'>
        <div className=''>
          <button className='flex outline outline-2 outline-gray-700 p-2 mr-2 bg-[#242E3A] rounded-full'>
            <div className=''>
            <svg xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 0 1-.659 1.591l-5.432 5.432a2.25 2.25 0 0 0-.659 1.591v2.927a2.25 2.25 0 0 1-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 0 0-.659-1.591L3.659 7.409A2.25 2.25 0 0 1 3 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0 1 12 3Z" />
            </svg>
            </div>
          </button>
        </div>
        <div className=''>
          <button className='flex outline outline-2 outline-gray-700 mr-2 bg-[#242E3A] rounded-full'>
            <div className=''>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-9">
              <path strokeLinecap="round" strokeLinejoin="round" d="M7.5 14.25v2.25m3-4.5v4.5m3-6.75v6.75m3-9v9M6" />
            </svg>

            </div>
          </button>
        </div>
        <div className=' bg-[#242E3A] outline outline-2 outline-gray-700 px-3 text-[12px] text-slate-300 py-2 rounded-3xl'>
          <button className=''>
            Коллекция
          </button>
        </div>
        <div className=' bg-[#242E3A] outline outline-2 outline-gray-700 px-3 text-[12px] text-slate-300 py-2 rounded-3xl'>
          <button className=''>
            Модель
          </button>
        </div>
        <div className='bg-[#242E3A] outline outline-2 outline-gray-700 px-3 text-[12px] text-slate-300 py-2 rounded-3xl'>
          <button className=''>
            Фон
          </button>
        </div>
      </div>
      <div className='ml-3 mr-4 grid grid-cols-2'>
        <Card text="59"  collection={collections[getRandomInt(0,6)]} nft_id={getRandomInt(1,3000)} />
        <Card text="59"  collection={collections[getRandomInt(0,6)]} nft_id={getRandomInt(1,3000)} />
        <Card text="59"  collection={collections[getRandomInt(0,6)]} nft_id={getRandomInt(1,3000)} />
        <Card text="59"  collection={collections[getRandomInt(0,6)]} nft_id={getRandomInt(1,3000)} />
        <Card text="59"  collection={collections[getRandomInt(0,6)]} nft_id={getRandomInt(1,3000)} />
        <Card text="59"  collection={collections[getRandomInt(0,6)]} nft_id={getRandomInt(1,3000)} />
        <Card text="59"  collection={collections[getRandomInt(0,6)]} nft_id={getRandomInt(1,3000)} />
        <Card text="59"  collection={collections[getRandomInt(0,6)]} nft_id={getRandomInt(1,3000)} />

      </div>
      <Menu />
    </div>
  );
}

