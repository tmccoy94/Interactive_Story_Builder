import { useState } from "react";

const ThemeInput = ({ onSubmitFunction }) => {
    const [theme, setTheme] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();

        if (!theme.trim() === "") {
            setError("Theme cannot be empty.");
            return;
        }
        onsubmit(theme);
    }
        
    return <div className="theme-input-container">
        <h2>Enter a Theme for Your Story</h2>
        <p>Provide a theme or topic for your story. This will help guide the story generation process.</p>

        <form onSubmit={handleSubmit}>
            <div className="input-group">
                <input 
                    type="text" 
                    value={theme} 
                    onChange={(e) => setTheme(e.target.value)} 
                    placeholder="enter a theme: Adventure, Mystery, Sci-Fi etc." 
                    className={error ? "input-error" : ""}
                />
                {error && <span className="error-message">{error}</span>}
                <button type="submit" className="generate-btn">Generate Story</button>
            </div>
        </form>
        {error && <p className="error-message">{error}</p>}
    </div>;
}
export default ThemeInput;