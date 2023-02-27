import { useState } from "react";
import { sendRequest } from "../services/anime.service";
import '../App.css';

const AnimeForm = () =>{
    const [prediction, setPrediction] = useState();
    const [formState, setFormState] = useState({
        Title: "",
        Genre: "",
        Synopsis: "",
        Type: "",
        Producer: "",
        Studio:""
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
            setPrediction("Successful, prediction is "+JSON.stringify(response.Rating)+".");
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
                        <input placeholder="Title" value={formState.Title} type="text" name="Title"/>
                        <input placeholder="Genre" value={formState.Genre} type="text" name="Genre"/>
                        <input placeholder="Synopsis" value={formState.Synopsis} type="text" name="Synopsis"/>
                        <input placeholder="Type" value={formState.Type} type="text" name="Type"/>
                        <input placeholder="Producer" value={formState.Producer} type="text" name="Producer"/>
                        <input placeholder="Studio" value={formState.Studio} type="text" name="Studio"/>
                        <input type="submit" value="SUBMIT"/>
                    </form>
                    <p>{prediction}</p>
                </div>
            </div>
        </div>
    )
}

export default AnimeForm;
