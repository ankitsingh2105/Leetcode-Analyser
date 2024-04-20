import React, { useEffect, useState } from 'react';
import "./App.css"

export default function App() {
  const [chartUrl, setChartUrl] = useState('');
  const [submission, setSubmission] = useState(null);
  const [rating, setRating] = useState([]);
  const [username, setUsername] = useState('ankitchauhan21');
  const [name, setname] = useState(null);
  const [avatar, setAvatar] = useState(null);
  useEffect(() => {
    async function fetchChart() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/chart?username=${username}`);
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setChartUrl(url);
      } catch (error) {
        console.error('Error fetching chart:', error);
      }
    }

    async function fetchSubmissions() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/submissions?username=${username}`);
        const json = await response.json();
        setSubmission(json.recentSubmissions);
      } catch (error) {
        console.error('Error fetching submissions:', error);
      }
    }

    async function fetchRating() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/rating?username=${username}`);
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setRating(url);
      } catch (error) {
        console.error('Error fetching rating:', error);
      }
    }
    async function getName() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/name?username=${username}`);
        const data = await response.json(); // Parse JSON response
        console.log("data is : ", data);
        setname(data.name); // Set the name state
        setAvatar(data.image); // Set the name state
      } catch (error) {
        console.error('Error fetching name:', error);
      }
    }

    getName();
    fetchRating();
    fetchSubmissions();
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


  const handleSearch = async () => {
    setChartUrl(null);
    setSubmission(null);
    setRating(null);
    setname(null);
    setAvatar(null);
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/chart?username=${username}`);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setChartUrl(url);
    } catch (error) {
      console.error('Error fetching chart:', error);
    }
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/submissions?username=${username}`);
      const json = await response.json();
      setSubmission(json.recentSubmissions);
    } catch (error) {
      console.error('Error fetching submissions:', error);
    }
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/rating?username=${username}`);
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setRating(url);
    } catch (error) {
      console.error('Error fetching rating:');
    }
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/name?username=${username}`);
      const data = await response.json(); // Parse JSON response
      console.log("data is : ", data);
      setname(data.name); // Set the name state
      setAvatar(data.image); // Set the name state
    } catch (error) {
      console.error('Error fetching name:', error);
    }
  };

  return (
    <>
      <center>
        <h1>Leetcode Analyser</h1>
      </center>
      <br />
      <br />
      <center>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder='Enter a valid leetcode user name' style={{ padding: "10px", fontSize: "15px" }} />
        <br /><br />
        <button onClick={handleSearch}>Search</button>
      </center>
      <br />
      <br />
      <center>
        <h3>
          {
            avatar == null ? <div style={{ fontSize: "10px" }} className="loader2"></div>
              :
              <img style={{ borderRadius: "30px", height: "50px", width: "50px" }} src={avatar} alt="" />
          }
        </h3>
        {
          name == null ?
            <div style={{ fontSize: "10px" }} className='loader2'></div>
            :
            <h2>
              {name}
            </h2>
        }
      </center>
      <br />
      <section className='graphSection'>
        <div>
          {!chartUrl ? <div className="loader"></div> : <img src={chartUrl} alt="Chart" />}
        </div>
        <div>
          {rating === null ? <div className="loader"></div> : <img src={rating} alt="ratingGraph" />}
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
        {submission === null ? (
          <div className='loader'></div>
        ) : (
          submission.map((elem, index) => {
            const { lang, title, statusDisplay } = elem;
            return (
              <section key={index} className="subCard">
                <div>{index + 1}.</div>
                <div>{title}</div>
                <div style={statusDisplay === 'Accepted' ? normalStyle : errorStyle}>{statusDisplay}</div>
                <div>{lang}</div>
              </section>
            );
          })
        )}
      </center>
    </>
  );
}
