import { About } from './about/About';
import { Certificates } from './ceritficates/Certificates';
import { Diploma } from './diploma/Diploma';

import styles from './Main.module.scss';

export const Main = () => {
    return (
        <main className={styles['main']}>
            <About />
            <Diploma />
            <Certificates/>
        </main>
    );
};
