import { useState, useEffect } from "react";
import {useParams, useNavigate} from "react-router-dom";
import axios from "axios";
import LoadingStatus from "./LoadingStatus";

const API_BASE_URL = "/api";

function StoryLoader() {
    const {id} = useParams();
    const navigate = useNavigate();
    const [story, setStory] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (id) {
            loadStory(id);
        }
    }, [id]);

    const loadStory = async (storyId) => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`);
            setStory(response.data);
            setLoading(false);
        } catch (err) {
            if (err.response && err.response.status === 404) {
                setError("Story not found.");
            } else {
                setError("An error occurred while loading the story.");
            }
        } finally {
            setLoading(false);
        }
    }

    const createNewStory = () => {
        navigate("/")
    }

    if (loading) {
        return <LoadingStatus theme={"story"} />;
    }

    if (error) {
        return (
            <div className="story-loader">
                <div>
                    <h2>Story Not Found</h2>
                    <p>{error}</p>
                    <button onClick={createNewStory}>Go to story generator</button>
                </div>
            </div>
        );
    }

    if (story) {
        return (
            <div className="story-loader">
                // TODO Display the story content
            </div>
        );
    }

}

export default StoryLoader;