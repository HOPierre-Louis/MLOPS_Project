import axios from "axios";

const backendUrl = "http://localhost:5000";

export const sendRequest = async (data) =>{
    const response = await axios.post(backendUrl, data)
    return response.data;
}