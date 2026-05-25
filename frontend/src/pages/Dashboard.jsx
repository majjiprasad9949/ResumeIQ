import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  resumeService,
  jobService,
  analysisService
} from '../services/api';

import LoadingSpinner from '../components/LoadingSpinner';

export default function Dashboard() {

  const [resumes,setResumes]=useState([]);
  const [jobs,setJobs]=useState([]);
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState('');
  const [selectedResume,setSelectedResume]=useState('');
  const [selectedJob,setSelectedJob]=useState('');
  const [analyzing,setAnalyzing]=useState(false);

  // PDF viewer states
  const [showResume,setShowResume]=useState(false);
  const [resumeUrl,setResumeUrl]=useState('');

  const navigate=useNavigate();


  useEffect(()=>{

    loadData();

  },[]);


  const loadData=async()=>{

    try{

      setLoading(true);

      const [resumesRes,jobsRes]=await Promise.all([

        resumeService.list(),
        jobService.list()

      ]);

      setResumes(

        resumesRes.data.results ||
        resumesRes.data ||
        []

      );

      setJobs(

        jobsRes.data.results ||
        jobsRes.data ||
        []

      );

    }

    catch(err){

      console.log(err);

      setError(

        'Failed to load data'

      );

    }

    finally{

      setLoading(false);

    }

  };


  const handleAnalyze=async()=>{

    if(

      !selectedResume ||
      !selectedJob

    ){

      setError(

        'Please select both resume and job description'

      );

      return;

    }


    try{

      setAnalyzing(true);

      setError('');

      const result=

      await analysisService.calculateScore(

        selectedResume,
        selectedJob

      );

      navigate(

        '/results',

        {

          state:{

            analysis:

            result.data

          }

        }

      );

    }

    catch(err){

      console.log(err);

      setError(

        'Failed to analyze'

      );

    }

    finally{

      setAnalyzing(false);

    }

  };


  const handleDeleteResume=async(id)=>{

    if(

      window.confirm(

        'Delete this resume?'

      )

    ){

      await resumeService.delete(id);

      loadData();

    }

  };


  const handleDeleteJob=async(id)=>{

    if(

      window.confirm(

        'Delete this job description?'

      )

    ){

      await jobService.delete(id);

      loadData();

    }

  };


  // PDF Resume Viewer
  if(showResume){

    return(

      <div className="p-6">

        <button

        onClick={()=>{

          setShowResume(false);

        }}

        className="bg-blue-600 text-white px-4 py-2 rounded mb-4"

        >

          ← Back

        </button>

<object

data={resumeUrl}

type="application/pdf"

className="w-full h-screen border rounded"

>

<div className="p-4">

<p>

PDF preview unavailable

</p>

<a

href={resumeUrl}

target="_blank"

rel="noreferrer"

className="text-blue-600 underline"

>

Open Resume

</a>

</div>

</object>

      </div>

    );

  }


  if(loading){

    return <LoadingSpinner/>

  }


  return(

<div className="max-w-6xl mx-auto">

<div className="mb-8">

<h1 className="text-4xl font-bold">

Dashboard

</h1>

<p className="text-gray-600">

Manage resumes and jobs

</p>

</div>


{error && (

<div className="bg-red-100 border border-red-400 text-red-700 p-3 rounded mb-4">

{error}

</div>

)}


<div className="grid grid-cols-2 gap-4 mb-8">

<button

onClick={()=>navigate(

'/upload-resume'

)}

className="bg-blue-600 text-white p-3 rounded"

>

+ Upload Resume

</button>


<button

onClick={()=>navigate(

'/upload-job'

)}

className="bg-green-600 text-white p-3 rounded"

>

+ Upload Job Description

</button>

</div>



<div className="bg-white rounded shadow p-6 mb-8">

<h2 className="text-2xl font-bold mb-4">

Analyze Resume

</h2>


<div className="grid grid-cols-2 gap-4 mb-4">

<select

value={selectedResume}

onChange={(e)=>setSelectedResume(

e.target.value

)}

className="border p-2"

>

<option value="">

Choose Resume

</option>

{

resumes.map(r=>(

<option

key={r.id}

value={r.id}

>

{r.title}

</option>

))

}

</select>


<select

value={selectedJob}

onChange={(e)=>setSelectedJob(

e.target.value

)}

className="border p-2"

>

<option value="">

Choose Job

</option>

{

jobs.map(j=>(

<option

key={j.id}

value={j.id}

>

{j.title}

</option>

))

}

</select>

</div>


<button

onClick={handleAnalyze}

disabled={analyzing}

className="w-full bg-purple-600 text-white p-3 rounded"

>

{

analyzing

?

'Analyzing...'

:

'Analyze Resume'

}

</button>

</div>



<div className="grid grid-cols-2 gap-6">

<div className="bg-white p-6 rounded shadow">

<h2 className="text-xl font-bold mb-4">

Resumes ({resumes.length})

</h2>

{

resumes.map(r=>(

<div

key={r.id}

className="flex justify-between border-b py-3"

>

<span>

{r.title}

</span>


<div className="flex gap-3">

<button

onClick={()=>{

setResumeUrl(

r.file_url

);

setShowResume(

true

);

}}

className="text-blue-500"

>

View

</button>


<button

onClick={()=>handleDeleteResume(

r.id

)}

className="text-red-500"

>

Delete

</button>

</div>

</div>

))

}

</div>



<div className="bg-white p-6 rounded shadow">

<h2 className="text-xl font-bold mb-4">

Jobs ({jobs.length})

</h2>


{

jobs.map(j=>(

<div

key={j.id}

className="flex justify-between border-b py-3"

>

<span>

{j.title}

</span>

<button

onClick={()=>handleDeleteJob(

j.id

)}

className="text-red-500"

>

Delete

</button>

</div>

))

}

</div>

</div>

</div>

);

}