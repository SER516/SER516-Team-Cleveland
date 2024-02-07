import { useState } from "react";
import { Button, Modal } from "react-bootstrap";

const CustomModal = ({ headerTitle, message, showModal }) => {
    const [show, setShow] = useState(true);

    const handleClose = () => {
        console.log("handle click");
        setShow(false);
    }
    
    return (
        <div
            className="modal show"
            style={{ display: 'block', position: 'initial' }}
        >
            <Modal show={showModal && show}>
                <Modal.Header closeButton>
                    <Modal.Title>{headerTitle}</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    <p>{message}</p>
                </Modal.Body>

                <Modal.Footer>
                    <Button variant="danger" onClick={() => handleClose()}>Close</Button>
                </Modal.Footer>
            </Modal>
        </div>
    )
}

export default CustomModal;