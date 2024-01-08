import React, {useEffect, useState} from 'react';
import './dropdown.scss';

const Dropdown = ({ elements, changeSelectedItem, selected }) => {
    const [selectedItem, setSelectedItem] = useState(selected);
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        console.log('selected', selected);
        console.log('selectedItem', selectedItem);
        setSelectedItem && setSelectedItem(selected);
    }, [selected, selectedItem]);

    const handleItemClick = (item) => {
        setSelectedItem(item);
        changeSelectedItem(item);
        setIsOpen(false);
    };

    return (
        <div className="dropdown">
            <button className="dropdown-button" onClick={() => setIsOpen(!isOpen)}>
                {selectedItem ? selectedItem : 'Select an item'}
            </button>
            {isOpen && (
                <div className="dropdown-content">
                    {elements.map((item) => (
                        <div
                            key={item}
                            className="dropdown-item"
                            onClick={() => handleItemClick(item)}
                        >
                            {item}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Dropdown;
