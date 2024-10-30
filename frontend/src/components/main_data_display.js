import AugmentList from "./augment_list";
import CurrentRoundButtons from "./cur_round_buttons";
import ListOfOptions from "./possible_options";
import { useState, setState } from "react";


export function MainDataDisplay() {

    const [dataFromChild, setRoundTypeFromChild] = useState(-1)
    const [augmentChosenId, setAugmentChosen] = useState(-1);
    const [listOfChosenAugments, setAugmentsChosen] = useState(new Map());

    function handleRoundTypeDataOnPressed(roundTypeButtonPressed) {
        alert('You clicked round ' + roundTypeButtonPressed);
        setRoundTypeFromChild(roundTypeButtonPressed)
    }

    function handleAugmentChosen(augmentChosen) {
        setRoundTypeFromChild(-1);
        console.log('Log from Parent:', augmentChosen, 'has been selected')
        setAugmentChosen(augmentChosen)
        
        let newMap = new Map([
            [augmentChosen._id,augmentChosen]
        ]);
        console.log('temp Augment MAP:',newMap)
        if (listOfChosenAugments.size == 0){
            console.log('listOfChosenAugments was intially empty')
            setAugmentsChosen(newMap)
        }else{
            console.log('listOfChosenAugments has something in it already')
            let newCombinedMap = new Map([
                ...listOfChosenAugments,
                ...newMap
            ]); 
            setAugmentsChosen(newCombinedMap)
        }
        console.log('Current Augment MAP:',listOfChosenAugments)
        
    }


    return (
        <div className="grid grid-cols-3 col-span-3 flex-row gap-2">
            <div className="flex h-[1088px] bg-red-400">
                <AugmentList listOfAugments={listOfChosenAugments} />
            </div>
            <div className="flex h-full bg-orange-400">
                <CurrentRoundButtons roundTypeButtonPressed={handleRoundTypeDataOnPressed} />
            </div>
            <div className="h-screen bg-pink-500 overflow-y-auto text-wrap">
                <ListOfOptions round={dataFromChild} sendDataToParentAugment={handleAugmentChosen} listOfCurrentAugments={listOfAugments} />
            </div>
            <div className=" h-full col-span-3 bg-yellow-300">
                <button
                    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                    onClick={() => {
                        setAugmentsChosen(new Map())
                    }}
                >
                    Reset
                </button>
            </div>
        </div>



    );
}