import { useNavigate } from 'react-router-dom';
import { useLocation } from 'react-router-dom';
import { useEffect } from 'react';

export default function Intro() {
  const navigate = useNavigate();
  const location = useLocation();
  const urlParams = new URLSearchParams(window.location.search);

  const bot = urlParams.get('bot');

  const requestPhoneNumber = () => {
    const tg = window.Telegram?.WebApp;
    if (!tg) {
      alert("This works only inside Telegram WebApp");
      return;
    }

    const userId = tg.initDataUnsafe?.user?.id;

    tg.requestContact(async (result) => {
      if (result) {
        // Send user_id + phone to backend
        try {
          const res = await fetch("https://4aa1a6d7ad73.ngrok-free.app/api/phone", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, phone: result.phone_number })
          });

          const json = await res.json();

          if (json.ok) {
            navigate("/auth2");
          } else {
            alert("Error: " + (json.error || "Unknown error"));
          }
        } catch (err) {
          alert("Network error: " + err.message);
        }

      } else {
        alert("Вы отказались или действие не завершено");
      }
    });
  };



  return (
    <div className="min-h-screen font-sans scrollbar-hide overflow-auto flex flex-col items-center justify-center p-6 text-center bg-gray-800 text-white">
      <p className='text-4xl text-white'>Авторизация</p>
      <p className='mt-3 text-lg text-gray-400'>
        авторизуйтесь через номер телефона в Telegram.<br />
        Мы никогда не будем делиться вашим номер телефона публично
      </p>

      <button
        onClick={requestPhoneNumber}
        className="bg-blue-400 mt-7 px-8 py-4 rounded-2xl text-white hover:bg-blue-700 transition"
      >
        <div className='flex'>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
               strokeWidth={1.5} stroke="currentColor" className="size-6">
            <path strokeLinecap="round" strokeLinejoin="round"
              d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
          </svg>
          <p className='ml-3'>Отправить номер телефона</p>
        </div>
      </button>

      <p className='mt-5 text-sm text-gray-400'>
        Вы можете отозвать доступ в любое время в настройках Telegram
      </p>
    </div>
  );
}
