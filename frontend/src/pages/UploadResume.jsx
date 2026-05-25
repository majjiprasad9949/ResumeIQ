import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { resumeService } from '../services/api';

export default function UploadResume() {

  const [file, setFile] = useState(null);

  const [title, setTitle] = useState('');

  const [error, setError] = useState('');

  const [loading, setLoading] = useState(false);

  const [dragActive, setDragActive] = useState(false);

  const navigate = useNavigate();


  const handleDrag = (e) => {

    e.preventDefault();

    e.stopPropagation();

    if (

      e.type === 'dragenter' ||

      e.type === 'dragover'

    ) {

      setDragActive(true);

    }

    else {

      setDragActive(false);

    }

  };


  const handleDrop = (e) => {

    e.preventDefault();

    e.stopPropagation();

    setDragActive(false);

    const files = e.dataTransfer.files;

    if (

      files &&

      files[0]

    ) {

      handleFile(files[0]);

    }

  };


  const handleFile = (

    selectedFile

  ) => {

    const validTypes = [

      'application/pdf',

      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',

      'text/plain'

    ];


    if (

      !validTypes.includes(

        selectedFile.type

      )

    ) {

      setError(

        'Please upload PDF, DOCX, or TXT'

      );

      return;

    }


    if (

      selectedFile.size >

      10 * 1024 * 1024

    ) {

      setError(

        'File size must be less than 10MB'

      );

      return;

    }

    setFile(

      selectedFile

    );

    setError('');

    setTitle(

      selectedFile.name.replace(

        /\.[^/.]+$/,

        ''

      )

    );

  };


  const handleSubmit = async (e) => {

    e.preventDefault();

    if (

      !file ||

      !title

    ) {

      setError(

        'Please select file and title'

      );

      return;

    }

    try {

      setLoading(true);

      setError('');

      console.log(

        'Uploading file:',

        file

      );

      console.log(

        'Title:',

        title

      );


      const response =

      await resumeService.upload(

        file,

        title

      );


      console.log(

        'UPLOAD SUCCESS:',

        response

      );


      navigate(

        '/dashboard'

      );

    }

    catch(err){

      console.log(

        'FULL ERROR:',

        err

      );

      console.log(

        'RESPONSE:',

        err?.response

      );

      console.log(

        'DATA:',

        err?.response?.data

      );

      console.log(

        'STATUS:',

        err?.response?.status

      );

      setError(

        JSON.stringify(

          err?.response?.data ||

          'Failed to upload resume'

        )

      );

    }

    finally{

      setLoading(false);

    }

  };


  return (

    <div className="max-w-2xl mx-auto">

      <div className="mb-8">

        <h1 className="text-4xl font-bold text-gray-900 mb-2">

          Upload Resume

        </h1>

        <p className="text-gray-600">

          Upload your resume to get started

        </p>

      </div>


      {error && (

        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">

          {error}

        </div>

      )}


      <form onSubmit={handleSubmit}>


        <div

          onDragEnter={handleDrag}

          onDragLeave={handleDrag}

          onDragOver={handleDrag}

          onDrop={handleDrop}

          className={`border-2 border-dashed rounded-lg p-12 text-center mb-6 transition ${
            dragActive
            ?
            'border-blue-500 bg-blue-50'
            :
            'border-gray-300'
          }`}

        >

          <div className="text-4xl mb-4">

            📁

          </div>

          <p className="text-gray-600 mb-2">

            Drag and drop your resume here

          </p>

          <p className="text-gray-500 text-sm mb-4">

            or

          </p>


          <label className="inline-block">

            <input

              type="file"

              accept=".pdf,.docx,.txt"

              onChange={(e)=>{

                if(

                  e.target.files[0]

                ){

                  handleFile(

                    e.target.files[0]

                  );

                }

              }}

              className="hidden"

            />

            <span className="bg-blue-600 text-white px-6 py-2 rounded cursor-pointer">

              Browse Files

            </span>

          </label>

        </div>


        {file && (

          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">

            <p className="text-green-800 font-semibold">

              ✓ File selected:

              {' '}

              {file.name}

            </p>

            <p className="text-green-700 text-sm">

              {(file.size/1024).toFixed(2)}

              KB

            </p>

          </div>

        )}


        <div className="mb-6">

          <label className="block text-gray-700 font-semibold mb-2">

            Resume Title

          </label>

          <input

            type="text"

            value={title}

            onChange={(e)=>{

              setTitle(

                e.target.value

              )

            }}

            className="w-full border rounded px-4 py-2"

          />

        </div>


        <button

          type="submit"

          disabled={loading}

          className="w-full bg-blue-600 text-white py-2 rounded"

        >

          {

            loading

            ?

            "Uploading..."

            :

            "Upload Resume"

          }

        </button>

      </form>

    </div>

  );

}