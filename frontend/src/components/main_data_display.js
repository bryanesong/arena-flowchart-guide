import AugmentList from "./augment_list";
import CurrentRoundButtons from "./cur_round_buttons";
import ListOfOptions from "./possible_options";
import { useState } from "react";


export function MainDataDisplay() {

    const [dataFromChild,setRoundTypeFromChild] = useState(-1)
    const [augmentChosenId, setAugmentChosen] = useState(-1);

    function handleRoundTypeDataOnPressed(roundTypeButtonPressed){
        alert('You clicked round '+roundTypeButtonPressed);
        setRoundTypeFromChild(roundTypeButtonPressed)
    }

    function handleAugmentIdChosen(augmentChosenId){
        console.log('Log from Parent:',augmentChosenId,'has been selected')
        setAugmentChosen(augmentChosenId)
    }

    return (
        <div className="grid grid-cols-3 col-span-3 flex-row gap-2">
            <div className="flex h-[1088px] bg-red-400">
                <AugmentList />
            </div>
            <div className="flex h-full bg-orange-400">
                <CurrentRoundButtons roundTypeButtonPressed={handleRoundTypeDataOnPressed}/>
            </div>
            <div className="max-h-screen bg-pink-500 overflow-y-auto text-wrap">
                <ListOfOptions round={dataFromChild} sendDataToParentAugmentId={handleAugmentIdChosen}/>
            </div>
            <div>
                Data:{dataFromChild}
            </div>
        </div>

    );
}