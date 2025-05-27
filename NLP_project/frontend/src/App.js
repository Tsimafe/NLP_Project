import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [products, setProducts] = useState([]);
  const [message, setMessage] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) return;

    setLoading(true);
    setProducts([]);
    setMessage('');
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/extract', { url });
      console.log('Ответ от бэка:', response.data);


      if (Array.isArray(response.data.products)) {
        setProducts(response.data.products);
        setMessage(response.data.message);
      } else {
        setError('Ошибка: неправильный формат ответа от сервера');
      }

      setHistory((prev) => [url, ...prev.filter((u) => u !== url)]);
    } catch (err) {
      setError('Ошибка при обработке URL.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <aside className="sidebar">
        <h2>История запросов</h2>
        <ul>
          {history.map((u, idx) => (
            <li key={idx} onClick={() => setUrl(u)}>{u}</li>
          ))}
        </ul>
      </aside>

      <main className="main">
        <header className="header">
          <h1>🧠 NLP Product Extractor</h1>
        </header>

        <form onSubmit={handleSubmit} className="form">
          <input
            type="text"
            placeholder="Вставь ссылку на страницу"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button type="submit">Извлечь</button>
        </form>

        {loading && <p>Загрузка...</p>}
        {error && <p className="error">{error}</p>}

        {/* Добавляем отображение сообщения */}
        {message && <p>{message}</p>}

        {products && products.length > 0 && (
          <div className="results">
            <h3>Найденные товары:</h3>
            <ul>
              {products.map((p, idx) => (
                <li key={idx}>{p}</li>
              ))}
            </ul>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
