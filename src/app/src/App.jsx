import './App.css';
import { Header } from './Header';
import { Content } from './Content';
import { Footer } from './Footer';

function App() {
  return (
    <div className="App">
      <Header title='Супер крутий сайт'/>
      <Content />
      <Footer />
    </div>
  );
}

export default App;
