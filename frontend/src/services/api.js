import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({

  baseURL: `${API_URL}/api`,

  headers: {

    'Content-Type': 'application/json',

  },

});


// Add token automatically

api.interceptors.request.use(

  (config) => {

    const token = localStorage.getItem(
      'access_token'
    );

    if (token) {

      config.headers.Authorization =
      `Bearer ${token}`;

    }

    return config;

  },

  (error) => Promise.reject(error)

);


// Authentication

export const authService = {

  register:(

    fullName,
    email,
    password

  ) =>

  api.post(

    '/users/register/',

    {

      username:fullName,
      email,
      password,
      password_confirm:password

    }

  ),


  login: async(

    email,
    password

  ) => {

    const response = await api.post(

      '/users/login/',

      {

        email,
        password

      }

    );

    if (

      response.data.access

    ){

      localStorage.setItem(

        'access_token',
        response.data.access

      );

      localStorage.setItem(

        'refresh_token',
        response.data.refresh

      );

    }

    return response;

  },


  logout:()=>{

    localStorage.removeItem(
      'access_token'
    );

    localStorage.removeItem(
      'refresh_token'
    );

  },


  getProfile:()=>

    api.get(

      '/users/me/'

    )

};


// Resume Service

export const resumeService = {

  upload:(

    file,
    title

  )=>{

    const formData =
    new FormData();

    formData.append(

      'file',
      file

    );

    formData.append(

      'title',
      title

    );

    return api.post(

      '/resumes/upload/',

      formData,

      {

        headers:{

          'Content-Type':

          'multipart/form-data'

        }

      }

    );

  },


  list:()=>

    api.get(

      '/resumes/'

    ),


  delete:(id)=>

    api.delete(

      `/resumes/${id}/`

    )

};


// Job Service

export const jobService = {

  upload:(

    content,
    title,
    company

  )=>

  api.post(

    '/jobs/upload/',

    {

      content,
      title,
      company

    }

  ),


  list:()=>

    api.get(

      '/jobs/'

    ),


  delete:(id)=>

  api.delete(

    `/jobs/${id}/`

  )

};


// Analysis Service

export const analysisService = {

  calculateScore:(

    resumeId,
    jobId

  )=>

  api.post(

    '/analysis/ats/calculate_score/',

    {

      resume_id:resumeId,

      job_id:jobId

    }

  )

};


export default api;