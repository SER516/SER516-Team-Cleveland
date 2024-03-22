import { useEffect, useState } from "react";

const formatDate = (dateString) => {
    const year = dateString.substring(0, 4);
    const month = dateString.substring(5, 7);
    const day = dateString.substring(8, 10);
    return `${month}/${day}/${year}`;
};

const CustomCard = ({ num, title, from, to, members }) => {
    const [membersName, setMembersName] = useState('');

    useEffect(() => {
        setMembersName(members.join(", "));
    }, [members]);

    const formattedFrom = formatDate(from);
    const formattedTo = formatDate(to);

    return (
        <div className="d-flex justify-content-center col-sm-8 offset-sm-3 cards">
            <div>
                <h1 style={{ alignItems: "center", justifyContent: "center", textAlign: "center", fontSize: "4rem" }}>{`${num}`}</h1>
                <h3 style={{ alignItems: "center", justifyContent: "center", textAlign: "center" }}>{title}</h3>
                <h6 style={{ alignItems: "center", justifyContent: "center", textAlign: "center" }}>
                    {
                        `Date: ${formattedFrom} to ${formattedTo}`
                    }
                </h6>
                <h6 style={{ alignItems: "center", justifyContent: "center", textAlign: "center" }}>
                    {
                        membersName && `Violations by - ${membersName}`
                    }
                </h6>
            </div>
        </div>
    )
}

export default CustomCard;