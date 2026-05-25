import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Login() {

    const [email,setEmail]=useState("");
    const [password,setPassword]=useState("");
    const [error,setError]=useState("");
    const [loading,setLoading]=useState(false);

    const {login}=useAuth();

    const navigate=useNavigate();


    async function handleSubmit(e){

        e.preventDefault();

        setError("");

        setLoading(true);

        try{

            const response = await login(

                email,
                password

            );

            console.log(response);

            navigate(

                "/dashboard"

            );

        }

        catch(err){

            setError(

                err?.response?.data?.detail ||

                "Login failed"

            );

        }

        finally{

            setLoading(false);

        }

    }


return(

<div className="min-h-screen flex">

{/* LEFT SIDE */}

<div className="hidden md:flex md:w-1/2 bg-gradient-to-br from-blue-600 to-purple-700 text-white flex-col justify-center items-center p-10">

<h1 className="text-5xl font-bold mb-6">

ResumeIQ

</h1>

<p className="text-xl text-center">

Boost your ATS score, identify missing skills,
analyze job matches, and improve your resume.

</p>

<div className="mt-10 text-center">

<div className="mb-3">

✓ ATS Score Analysis

</div>

<div className="mb-3">

✓ Missing Keywords Detection

</div>

<div className="mb-3">

✓ Skill Gap Analysis

</div>

<div>

✓ Resume Optimization

</div>

</div>

</div>



{/* RIGHT SIDE */}

<div className="w-full md:w-1/2 flex justify-center items-center bg-gray-100">

<div className="bg-white shadow-2xl rounded-2xl p-8 w-[420px]">

<h2 className="text-3xl font-bold text-center mb-2">

Welcome Back 

</h2>

<p className="text-center text-gray-500 mb-6">

Login to continue

</p>


{error && (

<div className="bg-red-100 text-red-700 p-3 rounded mb-4">

{error}

</div>

)}


<form onSubmit={handleSubmit}>


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

className="border rounded-lg w-full p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"

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

className="border rounded-lg w-full p-3 mb-5 focus:outline-none focus:ring-2 focus:ring-blue-500"

/>


<button

type="submit"

disabled={loading}

className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-semibold transition"

>

{

loading

?

"Logging in..."

:

"Login"

}

</button>

</form>


<p className="text-center mt-5">

New user?

<Link

to="/register"

className="text-blue-600 ml-1 font-semibold"

>

Register

</Link>

</p>

</div>

</div>

</div>

);

}