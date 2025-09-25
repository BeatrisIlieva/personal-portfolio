import styles from './About.module.scss';

import cvPdf from '../../../assets/cv.pdf';

export const About = () => {
    const handleDownloadCV = () => {
        const link = document.createElement('a');
        link.href = cvPdf;
        link.download = 'Beatris_Ilieva_CV.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <section id='beatris-ilieva' className={styles['about']}>
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
                        Plans to pursue AI and Machine Learning education
                        including data science and deep learning.
                    </p>
                </div>
            </div>

            <div className={styles['personal-photo']}>
                <div className={styles['thumbnail']}>
                    <img src='/personal-photo.png' alt='BeatrisIlieva' />
                </div>
                <button onClick={handleDownloadCV}>Download CV</button>
            </div>
        </section>
    );
};
