import styles from './About.module.scss';

export const About = () => {
    return (
        <section id='about' className={styles['about']}>
            <div className={styles['info']}>
                <div className={styles['wrapper-top']}>
                    <h1>
                        Full-stack developer
                        <span className={styles['dot']}></span>
                    </h1>

                    <p>
                        I like bringing both the technical and visual aspects
                        <br></br> of web applications to life.
                    </p>
                </div>

                <div className={styles['wrapper-bottom']}>
                    <p>
                        Building products with great user experience using
                        Django, React, and AI integrations.
                    </p>

                    <p>
                        Plans to pursue AI and Machine Learning education in
                        data science and deep learning.
                    </p>
                </div>
            </div>

            <div className={styles['personal-photo']}>
                <div className={styles['thumbnail']}>
                    <img src='/personal-photo.png' alt='BeatrisIlieva' />
                </div>
                <div className={styles['circle']}></div>
                <div className={styles['circle']}></div>
                <div className={styles['circle']}></div>
                <div className={styles['circle']}></div>
                <div className={styles['circle']}></div>
                <div className={styles['circle']}></div>
            </div>
        </section>
    );
};
