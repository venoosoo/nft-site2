import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import myImage from "./photo_2025-10-01_23-31-07.jpg";

export default function Menu() {
  const [userPhoto, setUserPhoto] = useState(null);
  const navigate = useNavigate();
  const location = useLocation(); // current path

  const [activeTab, setActiveTab] = useState(location.pathname); // track active tab

  useEffect(() => {
    if (window.Telegram?.WebApp) {
      const tg = window.Telegram.WebApp;
      tg.ready();
      const user = tg.initDataUnsafe?.user;
      if (user?.photo_url) {
        setUserPhoto(user.photo_url);
      }
    }
  }, []);

  const tabs = [
    { name: "Маркет", path: "/" },
    { name: "Мои подарки", path: "/gifts" },
    { name: "Сезон", path: "/auth" },
  ];

  const handleClick = (tab) => {
    setActiveTab(tab.path);
    navigate(tab.path);
  };

  return (
    <div className="fixed bottom-1 flex">
      <div className="flex gap-7 mb-2 ml-3 px-11 bg-[#1D2532] py-2 rounded-[40px] outline outline-1 outline-gray-600">
        {tabs.map((tab, index) => (
          <div key={index} className="flex flex-col items-center justify-center">
            <button
              className="items-center flex flex-col justify-center"
              onClick={() => handleClick(tab)}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke={activeTab === tab.path ? "#1A75DD" : "currentColor"} // highlight active
                className="w-6 h-6"
              >
                {/* You can customize the path for each icon */}
                {index === 0 && (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z"
                  />
                )}
                {index === 1 && (
                  <path
                    fill=""
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M21 11.25v8.25a1.5 1.5 0 0 1-1.5 1.5H5.25a1.5 1.5 0 0 1-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 1 0 9.375 7.5H12m0-2.625V7.5m0-2.625A2.625 2.625 0 1 1 14.625 7.5H12m0 0V21m-8.625-9.75h18c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125h-18c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z"
                  />
                )}
                {index === 2 && (
                  <path
                    fill="white"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09Z"
                  />
                )}
              </svg>
              <p
                className={`text-[10px] ml-1 ${
                  activeTab === tab.path ? "text-[#1A75DD]" : "text-white"
                }`}
              >
                {tab.name}
              </p>
            </button>
          </div>
        ))}
      </div>

      <div className="flex items-center justify-center mb-2 ml-5">
        {userPhoto ? (
          <img
            src={userPhoto}
            className="rounded-full h-[60px] w-[60px] items-center justify-center flex"
            alt="Telegram User"
          />
        ) : (
          <img className="rounded-full h-[60px] w-[60px] items-center justify-center flex" src={myImage} />
        )}
      </div>
    </div>
  );
}
