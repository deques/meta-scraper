import { useEffect, useState } from 'react'
import Givers from './components/givers';

function App() {
  const [chartData, setChartData] = useState([])
  const [loading, setLoading] = useState(true)

  const setDataset = (data) => {
    setChartData({
      labels: data.map((user) => user.name),
      datasets: [
        {
          label: "Given prizes",
          data: data.map((user) => user.prizes)
        }
      ]

    })
    setLoading(false)
  }
  const getData = async () => {
    const response = await fetch(
      "http://localhost:3000/giveaways/"
    );
    const json = await response.json();
    setDataset(json)
  };
  
  useEffect(()=> {
    getData();
  }, [])

  return (
    <div className="App">
      <h2>Hello</h2>
      {loading ? (
        <h2>Loading</h2>
      ) : (
        <Givers data={chartData} />
      )}
    </div>
  )
}

export default App
