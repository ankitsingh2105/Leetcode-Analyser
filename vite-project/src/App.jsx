import React, { useEffect, useState } from 'react';
import "./App.css"
import { combineReducers } from 'redux';
export default function App() {
  const [chartUrl, setChartUrl] = useState('');
  const [submission, setSubmission] = useState([]);
  const [rating, setrating] = useState([]);
  useEffect(() => {
    async function fetchChart() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/chart');
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setChartUrl(url);
      } catch (error) {
        console.error('Error fetching chart:', error);
      }
    }
    async function submission() {
      try {
        const response = await fetch("http://127.0.0.1:5000/api/submissions");
        const json = await response.json();
        setSubmission(json.recentSubmissions);
        console.log("this is the sub ", submission);
      }
      catch (error) {
        console.log("this is the error  : ", error);
      }
    }
    async function rating() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/rating');
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setrating(url);
      } catch (error) {
        console.error('Error fetching chart:', error);
      }
    }
    rating();
    submission();
    fetchChart();
  }, []);

  const errorStyle = {
    color: 'red',
    fontWeight: 'bold',
  };

  const normalStyle = {
    color: 'green',
    fontWeight: 'bold',
  };


  return (
    <>
      <center>
        <h1>Leetcode Analyser</h1>
      </center>
      <br />
      <br />
      <section className='graphSection'>
        <div>
          {
            !chartUrl ? <div className="loader"></div>
              :
              <img src={chartUrl} alt="Chart" />
          }
        </div>
        <div>
          {
            !rating ? <div className="loader"></div>
              :
              <img src={rating} alt="ratingGraph" />
          }
        </div>
      </section>
        <br />
      <center>
        <h1>Submissions</h1>
        <br /><br />
        <section style={{ background: "#e3e2e2" }} className="subCard">
          <div style={{ fontWeight: "bolder" }}>Sr. No.</div>
          <div style={{ fontWeight: "bolder" }}>Title</div>
          <div style={{ fontWeight: "bolder" }}>Status</div>
          <div style={{ fontWeight: "bolder" }}>Language</div>
        </section>
        {
          !submission ? <div className='loader'></div>
            :
            <>
              {
                submission.map((elem, index) => {
                  const { lang, title, statusDisplay } = elem;
                  return (
                    <>
                      <section key={index} className="subCard">
                        <div>{index + 1}.</div>
                        <div>{title}</div>
                        <div style={statusDisplay == 'Accepted' ? normalStyle : errorStyle}>{statusDisplay}</div>
                        <div>{lang}</div>
                      </section>
                    </>
                  )
                })
              }
            </>
        }
      </center>
    </>
  );
}
