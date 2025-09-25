import styles from './Diploma.module.scss';

export const Diploma = () => {
    return (
        <section id='education' className={styles['diploma']}>
            <p>
                Graduated from the{' '}
                <strong>Software Engineering with Python</strong> program at{' '}
                <em>Software University</em>, achieving excellent grades in all
                exams.
            </p>

            <div className={styles['wrapper']}>
                <div>
                    <a href='https://softuni.bg/certificates/details/250352/a3d65bbe'>
                        <img src='/diploma-1.jpeg' alt='diploma' />
                    </a>
                </div>

                <div>
                    <a href='https://softuni.bg/certificates/details/250352/a3d65bbe'>
                        <img src='/diploma-2.jpeg' alt='diploma' />
                    </a>
                </div>

                <div>
                    <a href='https://softuni.bg/certificates/details/250352/a3d65bbe'>
                        <img src='/diploma-3.jpeg' alt='diploma' />
                    </a>
                </div>
            </div>
        </section>
    );
};
