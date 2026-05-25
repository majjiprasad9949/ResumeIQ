import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Register() {

    const { register } = useAuth();

    const navigate = useNavigate();

    const [username,setUsername]=useState("");
    const [email,setEmail]=useState("");
    const [password,setPassword]=useState("");
    const [confirmPassword,setConfirmPassword]=useState("");
    const [error,setError]=useState("");
    const [loading,setLoading]=useState(false);


    async function handleSubmit(e){

        e.preventDefault();

        setError("");

        setLoading(true);

        try{

            await register(

                username,
                email,
                password,
                confirmPassword

            );

            navigate(

                "/login"

            );

        }

       catch(err){

    console.log(

        err.response?.data

    );

    const errorData =

    err.response?.data;

    if(errorData){

        const firstError =

        Object.values(

            errorData

        )[0];

        setError(

            Array.isArray(firstError)

            ?

            firstError[0]

            :

            firstError

        );

    }

    else{

        setError(

            "Registration failed"

        );

    }

}

        finally{

            setLoading(false);

        }

    }


return(

<div className="min-h-screen flex">

{/* LEFT SIDE */}

<div className="hidden md:flex md:w-1/2 bg-gradient-to-br from-purple-600 to-blue-700 text-white flex-col justify-center items-center p-10">

<h1 className="text-5xl font-bold mb-6">

ResumeIQ

</h1>

<p className="text-xl text-center">

Create your account and start optimizing
your resume with AI-powered analysis.

</p>


<div className="mt-10">

<div className="mb-3">

✓ Resume Upload

</div>

<div className="mb-3">

✓ ATS Score Analysis

</div>

<div className="mb-3">

✓ Skill Gap Detection

</div>

<div>

✓ Job Matching Insights

</div>

</div>

</div>



{/* RIGHT SIDE */}

<div className="w-full md:w-1/2 flex justify-center items-center bg-gray-100">

<div className="bg-white shadow-2xl rounded-2xl p-8 w-[420px]">

<h2 className="text-3xl font-bold text-center mb-2">

Create Account 

</h2>

<p className="text-center text-gray-500 mb-6">

Join ResumeIQ

</p>


{error && (

<div className="bg-red-100 text-red-700 p-3 rounded mb-4">

{error}

</div>

)}


<form onSubmit={handleSubmit}>

<label className="block mb-2 font-medium">

Username

</label>

<input

type="text"

placeholder="Enter username"

value={username}

onChange={(e)=>setUsername(

e.target.value

)}

className="border rounded-lg w-full p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-purple-500"

/>


<label className="block mb-2 font-medium">

Email

</label>

<input

type="email"

placeholder="Enter email"

value={email}

onChange={(e)=>setEmail(

e.target.value

)}

className="border rounded-lg w-full p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-purple-500"

/>


<label className="block mb-2 font-medium">

Password

</label>

<input

type="password"

placeholder="Enter password"

value={password}

onChange={(e)=>setPassword(

e.target.value

)}

className="border rounded-lg w-full p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-purple-500"

/>


<label className="block mb-2 font-medium">

Confirm Password

</label>

<input

type="password"

placeholder="Confirm password"

value={confirmPassword}

onChange={(e)=>setConfirmPassword(

e.target.value

)}

className="border rounded-lg w-full p-3 mb-5 focus:outline-none focus:ring-2 focus:ring-purple-500"

/>


<button

type="submit"

disabled={loading}

className="w-full bg-purple-600 hover:bg-purple-700 text-white p-3 rounded-lg font-semibold transition"

>

{

loading

?

"Creating Account..."

:

"Register"

}

</button>

</form>


<p className="text-center mt-5">

Already have an account?

<Link

to="/login"

className="text-purple-600 ml-1 font-semibold"

>

Login

</Link>

</p>

</div>

</div>

</div>

);

}