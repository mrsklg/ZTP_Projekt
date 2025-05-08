import { Icon } from 'react-icons-kit';
import {magnifying_glass} from 'react-icons-kit/ikons/magnifying_glass'
import {close} from 'react-icons-kit/ikons/close'
import '../styles/search.css'

export default function SerachBar({ query, onChange, onSearch, onClear }) {
    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            onSearch();
        }
    };

    return (
        <div className="search-bar">
            <Icon icon={magnifying_glass} className="search-icon"/>
            <input  type="text" 
                    placeholder="Search for title" 
                    value={query} 
                    onChange={onChange}
                    onKeyDown={handleKeyDown}/>
            {query && (
                <Icon
                    icon={close}
                    className="close-icon"
                    onClick={onClear}
                />
            )}
            <button onClick={onSearch}>Search</button>
        </div>
    )
}