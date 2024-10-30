import { cloneElement, useState, componentDidUpdate } from "react";

const test_data_augments = [
    {
        id: "123",
        name: "AugmentName1",
        stats: "Here are the stats1"
    },
    {
        id: "456",
        name: "AugmentName2",
        stats: "Here are the stats2"
    },
    {
        id: "789",
        name: "AugmentName3",
        stats: "Here are the stats3"
    }
]

const Augment = ({ id, name, desc }) =>
    <div>
        <li key={id}>
            <h2>{name}</h2>
            <p>{desc}</p>
        </li>
        <br />
    </div>

function getComponents({ listOfAugments }) {
    console.log('augment Has map checker!')
    const comps = [];
    listOfAugments.forEach((augment_values,augment_id) => comps.push({
        id: augment_id, 
        name: augment_values.name,
        desc: augment_values.desc, 
    }));
    return comps;
}



export default function AugmentList({ listOfAugments }) {
    console.log('Current Build Component, incoming augment:', listOfAugments)
    const displayArr = getComponents({listOfAugments})
    console.log("Display Array:",displayArr)
    return (
        <div className="border-2 w-max">
            <ol>
                <li>
                    {displayArr.map(Augment)}
                </li>
            </ol>
        </div>
    )
}
