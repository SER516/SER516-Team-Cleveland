import { useEffect, useState } from "react";

const CustomCard = ({ num, title, from, to, members }) => {
    const [membersName, setMembersName] = useState('');

    useEffect(() => {
        setMembersName(members.join(", "));
    }, [members]);

    return (
        <div className="d-flex justify-content-center col-sm-8 offset-sm-3 cards">
            <div>
                <h1 style={{ alignItems: "center", justifyContent: "center", textAlign: "center", fontSize: "4rem" }}>{`${num}`}</h1>
                <h3 style={{ alignItems: "center", justifyContent: "center", textAlign: "center" }}>{title}</h3>
                <h6 style={{ alignItems: "center", justifyContent: "center", textAlign: "center" }}>
                    {
                        `Date: ${from} to ${to}`
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