import { useState, useEffect } from "react";
import { authService } from "../services/api";

export function useAuth() {

    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const [loading, setLoading] = useState(true);


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

    ){

        const response = await authService.login(

            email,
            password

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

    ){

        const response = await authService.register(

            username,
            email,
            password
        );

        return response.data;

    }


    function logout(){

        authService.logout();

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