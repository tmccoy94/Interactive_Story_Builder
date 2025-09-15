import { useState } from "react";
import axios from "axios";

function StoryGenerator() {
    // 1. Create state for theme input and loading/error/story states
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [theme, setTheme] = useState("Pirate Party");
    const [story, setStory] = useState(null);

    // 3. Handle input changes

    // 4. Handle form submission (button click)
    // function handleSubmit(e) {
    //     const form = e.target;
    //     const formData = new FormData(form);

    //     console.log(formData)
    // }

    // 2. Render a text input for the theme
    return (
        <div>
            <div style={{display: "flex", justifyContent: "center", alignItems: "center"}}>
                <h3>
                    Select a theme for your story: 
                </h3>   
            </div>
            <div style={{display: "flex", justifyContent: "center", alignItems: "center", paddingTop: "2%"}}>
                <input 
                    name="StoryInput" 
                    defaultValue={theme}
                    onChange={e => setTheme(e.target.value)}
                    style={{
                        backgroundColor: "White", 
                        color: "Black",
                        padding: "10px",
                        fontSize: "16px",
                        borderRadius: "8px",
                        width: "40%",       // fixed width
                        boxSizing: "border-box" // makes padding included in width
                    }}
                />
            </div>
            <div style={{display: "flex", justifyContent: "center", alignItems: "center", paddingTop: "5%"}}>
                <button onClick={() => console.log(theme)} className="new-story-btn">
                    Create New Story
                </button>
            </div>
        </div>
    )

    // 5. Make POST request to backend to create story job

    // 6. Poll backend for job completion and fetch generated story

    // 7. Display loading, error, or story result
}

export default StoryGenerator;