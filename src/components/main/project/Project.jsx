import { Video } from './video/Video';
import styles from './Project.module.scss';

export const Project = () => {
    return (
        <section id='project' className={styles['project']}>
            <Video videoName='product-list' />
            <Video videoName='product-list' />
        </section>
    );
};
