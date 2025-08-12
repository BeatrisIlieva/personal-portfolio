import styles from './Diploma.module.scss';

export const Diploma = () => {
    return (
        <section id='diploma' className={styles['diploma']}>
            <div>
                <img src='/diploma-1.jpeg' alt='diploma' />
            </div>

            <div>
                <img src='/diploma-2.jpeg' alt='diploma' />
            </div>

            <div>
                <img src='/diploma-3.jpeg' alt='diploma' />
            </div>
        </section>
    );
};
