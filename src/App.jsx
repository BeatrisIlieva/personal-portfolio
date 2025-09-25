import { Header } from './components/header/Header';

import styles from './App.module.scss';
import { Main } from './components/main/Main';
import { Footer } from './components/footer/Footer';

function App() {
    return (
        <div className={styles['app']}>
            <Header />
            <Main />
            <Footer />
        </div>
    );
}

export default App;
