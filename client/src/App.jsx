import { Header } from './components/header/Header';

import styles from './App.module.scss';
import { Main } from './components/main/Main';

function App() {
    return (
        <div className={styles['app']}>
            <Header />
            <Main />
        </div>
    );
}

export default App;
