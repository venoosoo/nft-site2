import React, { useEffect, useState } from "react";


export default function Menu() {
  const [userPhoto, setUserPhoto] = useState(null);

  useEffect(() => {
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready(); // initialize

      const user = tg.initDataUnsafe?.user;
      if (user?.photo_url) {
        setUserPhoto(user.photo_url);
      } else {
        console.log("User has no profile photo.");
      }
    }
  }, []);

  return (
    <div className="fixed bottom-1 flex">
        <div className='  flex gap-5  mb-5 ml-5 px-6 bg-[#1D2532] p-3 rounded-[40px] outline outline-1 outline-gray-600'>
            <div className='flex flex-col items-center justify-center'>
                <button className='items-center flex flex-col justify-center'>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="blue" className="size-6">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
                    </svg>
                    <p className='text-sm ml-1 text-blue-600'>Маркет</p>
                </button>
            </div>
            <div className='flex flex-col items-center justify-center'>
                <button className='items-center flex flex-col justify-center'>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M21 11.25v8.25a1.5 1.5 0 0 1-1.5 1.5H5.25a1.5 1.5 0 0 1-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 1 0 9.375 7.5H12m0-2.625V7.5m0-2.625A2.625 2.625 0 1 1 14.625 7.5H12m0 0V21m-8.625-9.75h18c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125h-18c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
                    </svg>

                    <p className='text-sm ml-1'>Мои подарки</p>
                </button>
            </div>
            <div className='flex flex-col items-center justify-center'>
                <button className='items-center flex flex-col justify-center'>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-7 ">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259" />
                    </svg>
                    <p className='text-sm ml-1'>Сезон</p>
                </button>
            </div>
        </div>
        <div className="flex items-center justify-center mb-5">
            {userPhoto ? (
                <img src={userPhoto} className="rounded-full w-[70%] h-[70%] items-center justify-center flex" alt="Telegram User" />
            ) : (
                <p>no tg</p>
            )}
        </div>
    </div>
  );
}

