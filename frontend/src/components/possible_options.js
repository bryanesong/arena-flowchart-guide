// need to create a list of possible augments, default shows no augments
import { useState, useEffect, useCallback, useMemo } from "react";

const test_data_augments = [
    {
        name: 'augment1',
        desc: 'augment1 desc',
        stats: 'augment1 stats'
    },
    {
        name: 'augment2',
        desc: 'augment2 desc',
        stats: 'augment2 stats'
    },
    {
        name: 'augment3',
        desc: 'augment3 desc',
        stats: 'augment3 stats'
    }
];


export default function ListOfOptions({ round, sendDataToParentAugment, listOfCurrentAugments }) {
    const [augment_data, setAugmentData] = useState([]);

    /*
    const listOfAugments = test_data_augments.map(augment =>
        <li>
            <p>
                <b>{augment.name}:</b><br />
                Desc: {augment.desc} <br />
                Stats: {augment.tooltip} <br />
            </p>
        </li>
    );
    */

    useEffect(() => {
        const fetchAugments = async () => {
            try {
                console.log('Fetching API via POST Request.')
                const myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                console.log('list of current augments:',listOfCurrentAugments)
                var raw = JSON.stringify(listOfCurrentAugments);
                console.log('listOfCurrentAugments after JSONify',raw)
                if (listOfCurrentAugments.size == 0) {de
                    console.log("input list in empty")
                    raw = JSON.stringify([])
                }

                

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: raw,
                    redirect: "follow"
                };
                //console.log('Round:',round)
                const response = await fetch("http://localhost:8000/augments/match/" + round, requestOptions);


                if (!response.ok) {
                    setAugmentData([])
                } else {
                    //console.log('RESPONSE:', response)
                    const data = await response.json()

                    console.log('post request:', data)

                    let response_map = new Map(Object.entries(data['augments']));
                    //console.log('response augment data:',response_map)
                    let values_augments = Array.from(response_map.values());
                    //console.log('ARRAY of augments',values_augments)

                    setAugmentData(values_augments)
                }

            } catch (e) {
                console.log("ERROR:", e)
            }
            //var augment_json = JSON.parse(response);
            //listOfAugments
        }
        fetchAugments();
    }, [round]);//whenever variable changes that is specified in this array, component is re-rendered

    const [dataFromChild, setDataFromChild] = useState("");

    function handleDataFromChild(data) {
        console.log('subchild test:', data)
        sendDataToParentAugment(data)
    }

    return (
        <div>
            <div>
                <ol>
                    <AugmentList data={augment_data} sendDataToParentAugment={handleDataFromChild} />
                </ol>
            </div>

        </div>
    );
}


function AugmentList({ data, sendDataToParentAugment }) {
    const [query, setQuery] = useState("");
    const [augment_data, setAugmentData] = useState([]);

    const filteredItems = useMemo(() => {
        console.log('current data position:', data)
        if (data == null || data == undefined) {
            return null;
        }
        setAugmentData(data)
        if (query === "") return data;
        return data.filter(
            (item) => item.name.toLowerCase().search(query.toLowerCase()) !== -1
        ); // toLowerCase() to not care about case sensitivity
    }, [query, data]); // this will rerun when either query or allitems is changes


    function handleAugmentButtonClick(augment) {
        console.log("This augment was selected:", augment.name);
        sendDataToParentAugment(augment);
    }
    if (augment_data == undefined) {
        return <div>Waiting to next round to be selected.</div>
    }
    if (augment_data.length > 1) {
        return (
            <div>
                <div className="mb-3 xl:w-96">
                    <div className="relative mb-4 flex w-full flex-wrap items-stretch">
                        <input
                            type="text"
                            className="relative m-0 block flex-auto rounded border border-solid border-neutral-300 bg-transparent bg-clip-padding px-3 py-[0.25rem] text-base font-normal leading-[1.6] text-neutral-700 outline-none transition duration-200 ease-in-out focus:z-[3] focus:border-primary focus:text-neutral-700 focus:shadow-[inset_0_0_0_1px_rgb(59,113,202)] focus:outline-none dark:border-neutral-600 dark:text-neutral-200 dark:placeholder:text-neutral-200 dark:focus:border-primary"
                            placeholder="Search"
                            aria-label="Search"
                            aria-describedby="button-addon2"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                        />
                    </div>
                </div>
                <div>
                    <div>{filteredItems.map((augment) => (
                        <div>
                            <li>
                                <h1>
                                    <button
                                        class="relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-purple-600 to-blue-500 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800"
                                        onChange={data = null} //empty list and force user to pick next round
                                        onClick={() => {
                                            handleAugmentButtonClick(augment)
                                            data = null
                                        }}
                                    >
                                        <span class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-white dark:bg-gray-900 rounded-md group-hover:bg-opacity-0">
                                            {augment['name']}
                                        </span>
                                    </button></h1>
                                <h2>{augment.desc}</h2>
                                <p>{augment.tooltip}</p>
                            </li>
                            <br />
                        </div>
                    ))
                    }
                    </div>
                </div>

            </div>);
    } else {
        return <div>Waiting to next round to be selected.</div>
    }
}
