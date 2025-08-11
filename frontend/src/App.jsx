import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/movies")
      .then(res => setMovies(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>Movie Booking</h1>
      {movies.map(movie => (
        <div key={movie.id}>
          <h2>{movie.title}</h2>
          <p>Cinema: {movie.cinema}</p>
          <p>Showtimes: {movie.showtimes.join(", ")}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
