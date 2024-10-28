import { useState } from "react";


export default function CurrentRoundButtons({roundTypeButtonPressed}) {


    function handleClick(round_type) {
        console.log("button pressed with this round type"+round_type);
        roundTypeButtonPressed(round_type);
    }

    return (
        <div className="h-max space-y-4 gap-4 border-2">
            <ol className="space-y-4">
                <li>
                    <button 
                        class="bg-gray-500 hover:bg-gray-400 text-white font-bold py-2 px-4 border-b-4 border-gray-700 hover:border-gray-500 rounded w-full"
                        onClick={ () =>
                            handleClick(0)
                        }
                    >
                        Silver Augment
                    </button>
                </li>
                <li>
                    <button 
                        class="bg-yellow-500 hover:bg-gray-400 text-white font-bold py-2 px-4 border-b-4 border-yellow-700 hover:border-yellow-500 rounded w-full"
                        onClick={ () =>
                            handleClick(1)
                        }
                    >
                        Gold Augment
                    </button>
                </li>
                <li>
                    <button 
                        class="bg-purple-500 hover:bg-gray-400 text-white font-bold py-2 px-4 border-b-4 border-purple-700 hover:border-purple-500 rounded w-full"
                        onClick={ () =>
                            handleClick(2)
                        }    
                    >
                        Prismatic Augment
                    </button>
                </li>
                <li>
                    <button 
                        class="bg-blue-500 hover:bg-gray-400 text-white font-bold py-2 px-4 border-b-4 border-blue-700 hover:border-blue-500 rounded w-full"
                        onClick={ () =>
                            handleClick(3)
                        }
                    >
                        Buy Item
                    </button>
                </li>
                <li>
                    <button 
                        class="bg-green-500 hover:bg-gray-400 text-white font-bold py-2 px-4 border-b-4 border-green-700 hover:border-green-500 rounded w-full"
                        onClick={ () =>
                            handleClick(4)
                        }
                    >
                        Stat Shard
                    </button>
                </li>
            </ol>
        </div>
    );
}