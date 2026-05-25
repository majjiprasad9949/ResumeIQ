import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { analysisService } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import ScoreDisplay from '../components/ScoreDisplay';

export default function Results() {

const { resumeId, jobId } = useParams();

const navigate = useNavigate();

const location = useLocation();

const [analysis,setAnalysis]=useState(

location.state?.analysis || null

);

const [loading,setLoading]=useState(

!analysis

);

const [error,setError]=useState('');



useEffect(()=>{

if(!analysis){

loadAnalysis();

}

},[resumeId,jobId,analysis]);



const loadAnalysis=async()=>{

try{

setLoading(true);

const result=

await analysisService.calculateScore(

resumeId,
jobId

);

setAnalysis(

result.data

);

}

catch{

setError(

'Failed to load analysis'

);

}

finally{

setLoading(false);

}

};



const getScoreColor=(score)=>{

if(score>=80){

return "bg-green-500 text-white";

}

else if(score>=50){

return "bg-yellow-500 text-black";

}

else if(score>=40){

return "bg-orange-500 text-white";

}

return "bg-red-500 text-white";

};



const getBarColor=(score)=>{

if(score>=80){

return "bg-green-500";

}

else if(score>=50){

return "bg-yellow-500";

}

else if(score>=40){

return "bg-orange-500";

}

return "bg-red-500";

};



const getHiringChance=(score)=>{

if(score>=80){

return "90%";

}

else if(score>=50){

return "70%";

}

else if(score>=40){

return "50%";

}

return "20%";

};



if(loading){

return <LoadingSpinner/>

}


if(error){

return(

<div className="p-6">

<div className="bg-red-100 p-4 rounded">

{error}

</div>

</div>

)

}


return(

<div className="max-w-5xl mx-auto p-6">

<h1 className="text-4xl font-bold mb-2">

Analysis Results

</h1>

<p className="text-gray-500 mb-8">

Your resume ATS compatibility score

</p>



<div className="mb-8">

<ScoreDisplay

score={analysis.ats_score}

riskLevel={analysis.risk_level}

/>

</div>



{/* Extra Insights */}

<div className="grid md:grid-cols-3 gap-4 mb-8">

<div className="bg-white shadow rounded-lg p-5">

<h3 className="font-bold">

🏆 Hiring Chance

</h3>

<p className="text-3xl font-bold text-green-600">

{getHiringChance(

analysis.ats_score

)}

</p>

</div>


<div className="bg-white shadow rounded-lg p-5">

<h3 className="font-bold">

🎯 Match Level

</h3>

<div

className={`mt-3 px-3 py-2 rounded-full inline-block ${getScoreColor(

analysis.ats_score

)}`}

>

{analysis.risk_level}

</div>

</div>


<div className="bg-white shadow rounded-lg p-5">

<h3 className="font-bold">

💡 Resume Advice

</h3>

<p className="mt-2">

{analysis.recommendation}

</p>

</div>

</div>



{/* Score Breakdown */}

<div className="bg-white rounded shadow p-6 mb-8">

<h2 className="text-2xl font-bold mb-5">

Score Breakdown

</h2>


{

[

{

label:"Keyword Match",

score:analysis.keyword_match_score

},

{

label:"Skills Match",

score:analysis.skills_match_score

},

{

label:"Resume Structure",

score:analysis.resume_structure_score

},

{

label:"Experience Match",

score:analysis.experience_match_score

},

{

label:"Grammar Quality",

score:analysis.grammar_quality_score

}

].map((item,index)=>(

<div key={index} className="mb-5">

<div className="flex justify-between mb-1">

<span>

{item.label}

</span>

<span className="font-bold">

{item.score}/100

</span>

</div>

<div className="w-full bg-gray-200 h-3 rounded-full">

<div

className={`h-3 rounded-full ${getBarColor(item.score)}`}

style={{

width:`${item.score}%`

}}

>

</div>

</div>

</div>

))

}

</div>



{/* Missing Keywords */}

<div className="bg-white rounded shadow p-6 mb-8">

<h2 className="text-2xl font-bold mb-4">

Missing Keywords

</h2>

<div className="flex flex-wrap gap-2">

{

analysis.missing_keywords?.map(

(keyword,index)=>(

<span

key={index}

className="bg-yellow-100 px-3 py-2 rounded-full"

>

{keyword}

</span>

)

)

}

</div>

</div>



{/* Suggested Roles */}
{/* Suggested Roles */}

<div className="bg-white rounded shadow p-6 mb-8">

<h2 className="text-2xl font-bold mb-4">

🎯 Recommended Roles

</h2>

<div className="flex flex-wrap gap-3">

{

analysis.ats_score >= 80 ? (

<>

{

analysis.matched_keywords?.includes(

"business analyst"

) && (

<span className="bg-green-100 px-4 py-2 rounded-full">

Business Analyst

</span>

)

}

{

analysis.matched_keywords?.includes(

"data analyst"

) && (

<span className="bg-blue-100 px-4 py-2 rounded-full">

Data Analyst

</span>

)

}

{

analysis.matched_keywords?.includes(

"analytics"

) && (

<span className="bg-purple-100 px-4 py-2 rounded-full">

Product Analyst

</span>

)

}

</>

)

:

analysis.ats_score >=50 ? (

<>

<span className="bg-yellow-100 px-4 py-2 rounded-full">

Junior Analyst

</span>

<span className="bg-yellow-100 px-4 py-2 rounded-full">

Associate Analyst

</span>

</>

)

:

(

<div className="bg-red-50 p-4 rounded w-full">

<h3 className="font-bold text-red-600">

No role recommendations available

</h3>

<p className="mt-2 text-gray-600">

Improve missing skills before applying.

</p>

</div>

)

}

</div>

</div>




<div className="flex gap-4">

<button

onClick={()=>navigate(

'/dashboard'

)}

className="flex-1 bg-blue-600 text-white py-3 rounded"

>

Back to Dashboard

</button>


<button

onClick={()=>window.print()}

className="flex-1 bg-gray-700 text-white py-3 rounded"

>

Print Results

</button>

</div>

</div>

)

}