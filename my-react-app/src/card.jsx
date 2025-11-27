import { cloneElement, useEffect, useState } from "react";



export default function Card(collection) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  
  var nft_id = collection.nft_id
  // Telegram NFT link we want backend to fetch
  const nftUrl = `https://fragment.com/gift/${collection.collection}-${nft_id}`;

  useEffect(() => {
    async function loadNFT() {
      try {
        // Call your Flask API instead of Telegram directly
        const apiUrl = `https://4aa1a6d7ad73.ngrok-free.app/api/nft?url=${encodeURIComponent(
          nftUrl
        )}`;

        const res = await fetch(apiUrl);
        if (!res.ok) throw new Error("HTTP " + res.status);
        const json = await res.json();
        setData(json)
      } catch (err) {
        setError(err.message);
      }
    }

    loadNFT();
  }, []);

  return (
  <div className="p-2 bg-gray-900 text-white mt-1 overflow-hidden">

    {error && <p>Error: {error}</p>}

    {!data && !error && (
      // Skeleton loader
      <div className="bg-[#1D2532] rounded-2xl outline outline-2 outline-gray-600 overflow-hidden animate-pulse">
        <div className="h-40 bg-gray-700 w-full"></div> {/* image placeholder */}
        <div className="p-3">
          <div className="h-5 bg-gray-700 rounded w-3/4 mb-2"></div> {/* title */}
          <div className="h-4 bg-gray-600 rounded w-1/4 mb-4"></div> {/* id */}
          <div className="flex items-center">
            <div className="h-8 bg-blue-700 rounded-3xl w-3/5 mr-2"></div> {/* button */}
            <div className="h-8 w-8 bg-gray-700 rounded-full"></div> {/* icon */}
          </div>
        </div>
      </div>
    )}

    {data && (
      <div className="bg-[#1D2532] rounded-2xl outline outline-2 outline-gray-600 overflow-hidden font-semibold">
        {data.image && (
          <img
            src={data.image}
            alt="nft preview"
            className="w-full"
          />
        )}
        <div> 
          <h1 className="text-lg ml-3 mt-2">{data.title || data.name}</h1>
          <h1 className="text-sm ml-3 text-gray-400">#{data.gift_id}</h1>
        </div>
        <div className="flex pb-3 items-center justify-center">
          <div className={` ${
                    collection.text ? "mt-4 bg-[#0080FF] h-fit w-[90%] py-0.5 rounded-3xl px- flex items-center justify-center" : 
                    "ml-2 mt-4 bg-[#0080FF] h-fit w-[60%] py-0.5 rounded-3xl px-1 flex items-center justify-center"
                }`}
                >
            <button
                className={` ${
                    collection.text ? "text-[16px] py-1 w-full" : "text-[15px] ml-4 "
                }`}
                >
                {collection.text ? collection.text : Math.round(Number(data.price.replace(/,/g, "")) * 10) / 10}
            </button>
            { (!collection.text) && ( <svg width="30" height="30" viewBox="0 0 60 57" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M28 56C43.464" fill="#0088CC"></path>
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M20.199 18.4844H35.9034C36.459 18.4844 37.0142 18.566 37.5944 18.8365C38.2899 19.1606 38.6587 19.6717 38.9171 20.0496C38.9372 20.079 38.956 20.1093 38.9734 20.1403C39.2772 20.6811 39.4338 21.265 39.4338 21.8931C39.4338 22.4899 39.2918 23.1401 38.9734 23.7068C38.9704 23.7122 38.9673 23.7176 38.9642 23.723L29.0424 40.7665C28.8236 41.1423 28.4209 41.3729 27.986 41.3714C27.5511 41.3698 27.15 41.1364 26.9339 40.759L17.1943 23.7518C17.1915 23.7473 17.1887 23.7426 17.1859 23.738C16.963 23.3707 16.6183 22.8027 16.558 22.0696C16.5026 21.3956 16.6541 20.7202 16.9928 20.1346C17.3315 19.5489 17.8414 19.0807 18.4547 18.7941C19.1123 18.4868 19.7787 18.4844 20.199 18.4844ZM26.7729 20.9192H20.199C19.7671 20.9192 19.6013 20.9458 19.4854 21C19.3251 21.0748 19.1905 21.1978 19.1005 21.3535C19.0105 21.5092 18.9698 21.6896 18.9846 21.8701C18.9931 21.9737 19.0353 22.0921 19.2842 22.5026C19.2894 22.5112 19.2945 22.5199 19.2995 22.5286L26.7729 35.5785V20.9192ZM29.2077 20.9192V35.643L36.8542 22.5079C36.9405 22.3511 36.999 22.1245 36.999 21.8931C36.999 21.7054 36.9601 21.5424 36.8731 21.3743C36.7818 21.2431 36.7262 21.1736 36.6797 21.126C36.6398 21.0853 36.6091 21.0635 36.5657 21.0433C36.3849 20.959 36.1999 20.9192 35.9034 20.9192H29.2077Z" fill="white"></path>
            </svg>
            )}
          </div>
          {(!collection.text) && (<div className="items-center flex ml-auto w-10 h-10 mr-3 mt-4 bg-[#304D68] rounded-full p-2"> 
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-7">
                <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
            </svg>
          </div>)}
        </div>
      </div>
    )}
  </div>
);

}
