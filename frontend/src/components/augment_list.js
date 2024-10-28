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

const Augment = ({ id, name, stats }) =>
    <div>
        <li key={id}>
            <h2>{name}</h2>
            <p>{stats}</p>
        </li>
        <br />
    </div>



export default function AugmentList() {
    return (
        <div className="border-2 w-max">
            <ul>
                {test_data_augments.map(Augment)}
            </ul>

        </div>
    )
}
