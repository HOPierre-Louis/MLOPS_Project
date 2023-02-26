import { useState } from "react";
import { sendRequest } from "../services/anime.service";
import '../App.css';

const AnimeForm = () =>{
    const [prediction, setPrediction] = useState();
    const [formState, setFormState] = useState({
        title: "",
        genre: "",
        description: "",
        type: "",
        producer: "",
        studio:""
    });

    const formChangeHandler = (event) => {
        setFormState({
            ...formState,
            [event.target.name]:event.target.value,
        });
    }


    const formSubmitHandler = (event) => {
        event.preventDefault();
        console.log(formState);
        sendRequest(formState).then(response => {
            setPrediction("Successful, prediction is "+JSON.stringify(response.pred)+".");
        }).catch(error =>{
            setPrediction("Error: "+ error.response.data+".");
            console.log(error);
        });

    }

    return(
        <div className="background">
            <div className="container">
                <div className = "form-box">
                    <form onChange={formChangeHandler} onSubmit={formSubmitHandler}>
                        <input placeholder="Title" value={formState.title} type="text" name="title"/>
                        <input placeholder="Genre" value={formState.genre} type="text" name="genre"/>
                        <input placeholder="Description" value={formState.description} type="text" name="description"/>
                        <input placeholder="Type" value={formState.type} type="text" name="type"/>
                        <input placeholder="Producer" value={formState.producer} type="text" name="producer"/>
                        <input placeholder="Studio" value={formState.studio} type="text" name="studio"/>
                        <input type="submit" value="SUBMIT"/>
                    </form>
                    <p>{prediction}</p>
                </div>
            </div>
        </div>
    )
}

export default AnimeForm;