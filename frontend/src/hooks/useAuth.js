import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/users";

export function useAuth() {

    const [

        isAuthenticated,

        setIsAuthenticated

    ] = useState(false);


    const [

        loading,

        setLoading

    ] = useState(true);


    useEffect(() => {

        const token = localStorage.getItem(
            "access_token"
        );

        setIsAuthenticated(
            !!token
        );

        setLoading(false);

    }, []);



    async function login(

        email,

        password

    ) {

        console.log(
            "Sending login request"
        );

        const response = await axios.post(

            `${API_URL}/login/`,

            {

                email,
                password

            }

        );

        console.log(
            "Backend response:",
            response.data
        );


        localStorage.setItem(

            "access_token",

            response.data.access

        );


        localStorage.setItem(

            "refresh_token",

            response.data.refresh

        );


        setIsAuthenticated(
            true
        );

        return response.data;

    }



    async function register(

        username,
        email,
        password,
        password_confirm

    ) {

        const response = await axios.post(

            `${API_URL}/register/`,

            {

                username,
                email,
                password,
                password_confirm

            }

        );

        return response.data;

    }



    function logout(){

        localStorage.removeItem(
            "access_token"
        );

        localStorage.removeItem(
            "refresh_token"
        );

        setIsAuthenticated(
            false
        );

    }


    return {

        isAuthenticated,

        loading,

        login,

        register,

        logout

    };

}